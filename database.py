import psycopg2
import psycopg2.extras
import utils
import numpy as np
import pandas as pd
import pymongo
from argparse import ArgumentParser
from collections import defaultdict


class CollegeQuery:
    #Sets up access to both psql database and mongo database
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.myclient['college_sport']

    def check_connectivity(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM college LIMIT 1")
        records = cursor.fetchall()
        return len(records) == 1

    def query_with_params(self, query, params = {}):
        self.cursor.execute(query, params)
        rst = self.cursor.fetchall()
        return rst
    # Simple query caller for mongo takes in the collection to work with and the query
    def query_mongo(self, collection, query):
        my_col = self.db[collection]
        my_doc = my_col.find(query)
        return my_doc

    # Diversity Query on GUI
    def diversity_query(self, limit):
        #Checks if user inputed a limit on the GUI uses one of two queries if they didn't (Both queries do the same thing just the
        #amount of results is different). This query outputs the total amount of minorities enrolled in a school along with the possible tuition
        #order by minorities enrolled
        if limit.isdigit():
            query = """
            SELECT ce.collegeid AS college, c.state, ce.enrollment_total AS minorities_enrolled, ct.in_state, ct.out_of_state
            FROM college c, (SELECT collegeid, SUM(enrollment) AS enrollment_total
                             FROM college_diversity cd
                             GROUP BY cd.collegeid) AS ce
            JOIN college_tuition ct ON ct.collegeid = ce.collegeid
            WHERE ce.collegeid = c.collegeid
            ORDER BY ce.enrollment_total DESC
            LIMIT %(limit)s;
            """
            params = {'limit': limit}
            diversity_query_results = self.query_with_params(query,params)
        else:
            query = """
            SELECT ce.collegeid AS college, c.state, ce.enrollment_total AS minorities_enrolled, ct.in_state, ct.out_of_state
            FROM college c, (SELECT collegeid, SUM(enrollment) AS enrollment_total
                             FROM college_diversity cd
                             GROUP BY cd.collegeid) AS ce
            JOIN college_tuition ct ON ct.collegeid = ce.collegeid
            WHERE ce.collegeid = c.collegeid
            ORDER BY ce.enrollment_total DESC;
            """
            diversity_query_results = self.query_with_params(query)

        #All results are put in pandas to look nicer
        query_result_df = pd.DataFrame(diversity_query_results, columns=['college', 'state', 'Minorities Enrolled',
        'In State Tuition', 'Out Of State Tuition'])
        print(query_result_df)

    # Career Stem Query on GUI
    def career_query(self, limit, state):
        #Queries percent of stem students and early career salary and organizes the results by the amount of students in stem.
        #There are multiple queries so the user can choose if they want to limit the results and if they want to only have results
        #For a specific state
        if limit.isdigit() and state:
            query = """
            SELECT cst.collegeid, c.state, cst.percent_stem, cs.early_career
            FROM college_students cst
            JOIN college c ON c.collegeid = cst.collegeid
            JOIN college_salary cs ON cs.collegeid = cst.collegeid
            WHERE cst.percent_stem IS NOT NULL
            AND c.state = %(state)s
            ORDER BY percent_stem DESC
            LIMIT %(limit)s;
            """
            params = {'limit': limit, 'state': state }
            career_query_results = self.query_with_params(query,params)
        elif limit.isdigit() and not state:
            query = """
            SELECT cst.collegeid, c.state, cst.percent_stem, cs.early_career
            FROM college_students cst
            JOIN college c ON c.collegeid = cst.collegeid
            JOIN college_salary cs ON cs.collegeid = cst.collegeid
            WHERE cst.percent_stem IS NOT NULL
            ORDER BY percent_stem DESC
            LIMIT %(limit)s;
            """
            params = {'limit' : limit}
            career_query_results = self.query_with_params(query, params)
        elif not limit.isdigit() and state:
            query = """
            SELECT cst.collegeid, c.state, cst.percent_stem, cs.early_career
            FROM college_students cst
            JOIN college c ON c.collegeid = cst.collegeid
            JOIN college_salary cs ON cs.collegeid = cst.collegeid
            WHERE cst.percent_stem IS NOT NULL
            AND c.state = %(state)s
            ORDER BY percent_stem DESC;
            """
            params = {'state':state}
            career_query_results = self.query_with_params(query, params)
        else:
            query = """
            SELECT cst.collegeid, c.state, cst.percent_stem, cs.early_career
            FROM college_students cst
            JOIN college c ON c.collegeid = cst.collegeid
            JOIN college_salary cs ON cs.collegeid = cst.collegeid
            WHERE cst.percent_stem IS NOT NULL
            ORDER BY percent_stem DESC;
            """
            career_query_results = self.query_with_params(query)

        #All results are put in pandas to look nicer
        query_result_df = pd.DataFrame(career_query_results, columns=['college', 'state', 'percent of student in stem',
        'early career salary'])
        print(query_result_df)

    #Winning Enrolled Query on GUI
    def team_query(self, win_percent, enrolled):
        #Need defaults in case user does not put anything
        if not win_percent:
            win_percent = .5
        if not enrolled:
            enrolled = 2000
        win_percent = float(win_percent)
        enrolled = int(enrolled)

        #MongoDB queries, since non-relational two seperate queies to see if win percent is greater then user inputed on
        #Results are put into a set to make sure there are no repeats and then put in array form for psql
        my_query = {'Win Percent': {'$gt' : win_percent}}
        basketball_dict = self.query_mongo('basketball', my_query)
        football_dict = self.query_mongo('football', my_query)
        teams_set = set()
        basketball_set = set()
        football_set = set()
        for i in basketball_dict:
            basketball_set.add('%'+str(i['Team'])+'%')
        for i in football_dict:
            football_set.add('%'+str(i['Team'])+'%')
        teams = list(basketball_set.intersection(football_set))

        #PSQL query to see if results exist in tables along with user inputed enrolled and what type of school
        query = """
        SELECT c.collegeid, c.state, cs.enrolled, cs.type
        FROM college c, college_statistics cs
        WHERE c.collegeid = cs.collegeid
        AND c.collegeid LIKE ANY(%(teams)s)
        AND enrolled >= %(enrolled)s
        ORDER BY cs.enrolled;
        """
        params = {'teams': teams, 'enrolled': enrolled}
        query_results = self.query_with_params(query,params)

        #All results are put in pandas to look nicer
        query_result_df = pd.DataFrame(query_results, columns=['college', 'state', 'enrolled', 'public or private'])
        print(query_result_df)

    # Grad Rate Query on GUI
    def worst_grad_rate_query(self, samples):
        if not samples:
            samples = 5
        samples = int(samples)
        # query average results of grad_rate, number of fulltime undergrads, in state tuition, out state tuition and students
        # who believe they are making a difference, allows user options to have a minimum of samples in each state
        query = """
            SELECT c.state, ROUND(AVG(CAST(cs.grad_rate AS NUMERIC)),2) AS grad_rate_avg, ROUND(AVG(CAST(cs.fulltime_undergrad AS NUMERIC)),2) AS fulltime_undergrad_AVG,
            ROUND(AVG(CAST(ct.in_state AS NUMERIC)),2) AS in_state_avg, ROUND(AVG(CAST(ct.out_of_state AS NUMERIC)),2) AS out_of_state_avg,
            ROUND(AVG(CAST(csa.making_a_difference AS NUMERIC)),2) AS making_a_difference_avg
            FROM college_students cs, college c, college_tuition ct, college_salary csa
            WHERE c.collegeid = cs.collegeid
            AND c.collegeid = ct.collegeid
            AND c.collegeid = csa.collegeid
            GROUP BY c.state
            HAVING COUNT(cs.grad_rate) > %(samples)s
            ORDER BY grad_rate_avg ASC;
            """
        params = {'samples':  samples}
        worst_grad_results = self.query_with_params(query, params)

        #All results are put in pandas to look nicer
        query_result_df = pd.DataFrame(worst_grad_results, columns=['State', 'Grad Rate AVG', 'Fulltime Undergrad AVG',
        'In State Tuition AVG', 'Out Of State Tuition AVG', 'Making A Difference AVG' ])
        print(query_result_df)

    # Winning Tech Query on GUI
    def sport_query(self, limit, power_rating, offensive_rank):
        if not power_rating:
            power_rating = .8
        if not offensive_rank:
            offensive_rank = 10
        #MongoDB queries, basketball query checks if it has a certain power rating (likelihood of beating a D1 team) and if they made the playoffs.
        #Football query checks if a team that had more losses than wins had a certain offensive rank
        #Results are put into a set to make sure there are no repeats and then put in array form for psql
        my_query_basketball = {'$and' : [{ 'Power Rating': { '$gt' : float(power_rating)}}, {'Playoff.Wins Cutoff': { '$gt' : 0}}]}
        my_query_football = {'$and': [{ '$expr' : { '$gt' : ["$Loss", "$Win"]} } , {'Offensive.Rank': { '$lt' : int(offensive_rank)}}]}
        basketball_dict = self.query_mongo('basketball', my_query_basketball)
        football_dict = self.query_mongo('football', my_query_football)
        teams_set = set()
        basketball_set = set()
        football_set = set()
        for i in basketball_dict:
            basketball_set.add('%'+str(i['Team'])+'%')
        for i in football_dict:
            football_set.add('%'+str(i['Team'])+'%')
        teams = list(basketball_set.intersection(football_set))

        #Option to limit results both queries check if a school that's true for either the football or basketball mongo query has professors with a phd or
        #students in stem
        if limit:
            query = """
            SELECT c.collegeid, c.state, cs.professor_with_phd, cst.percent_stem
            FROM college c, college_statistics cs, college_students cst
            WHERE c.collegeid = cs.collegeid
            AND c.collegeid = cst.collegeid
            AND c.collegeid LIKE ANY(%(teams)s)
            AND cst.percent_stem IS NOT NULL
            ORDER BY cs.professor_with_phd DESC, cst.percent_stem
            LIMIT %(limit)s;
            """
            params = {'teams': teams, 'limit' : int(limit)}

        else:
            query = """
            SELECT c.collegeid, c.state, cs.professor_with_phd, cst.percent_stem
            FROM college c, college_statistics cs, college_students cst
            WHERE c.collegeid = cs.collegeid
            AND c.collegeid = cst.collegeid
            AND c.collegeid LIKE ANY(%(teams)s)
            AND cst.percent_stem IS NOT NULL
            ORDER BY cs.professor_with_phd DESC, cst.percent_stem;
            """
            params = {'teams': teams}

        query_results = self.query_with_params(query,params)

        #All results are put in pandas to look nicer
        query_result_df = pd.DataFrame(query_results, columns=['College', 'State', 'Professors with PhD', 'Percent of students in Stem'])
        print(query_result_df)
