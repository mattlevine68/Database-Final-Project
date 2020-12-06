# - Five separate queries
# - At least two queries that select at least some data from both of your datasets
# - At least two queries that showcase syntax beyond the basic `SELECT-FROM-WHERE` clauses (e.g., Grouping, Subqueries, etc.)
# - At least two queries that accept input entered by the user (as opposed to just allowing selection from a list of options)

import psycopg2
import psycopg2.extras
import utils
import numpy as np
import pandas as pd
import pymongo
from argparse import ArgumentParser
from collections import defaultdict


class CollegeQuery:

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

    def print_records(self, records):
        for record in records:
            print(record)

    def query_mongo(self, table, query):
        my_col = self.db[table]
        my_doc = my_col.find(query)
        rst = []
        return my_doc

    # Which school and state has the most diversity and whats the tuition
    def diversity_query(self, Limit):
        if Limit.isdigit():
            query = """
            SELECT ce.collegeid AS college, c.state, ce.enrollment_total AS minorities_enrolled, ct.in_state, ct.out_of_state
            FROM college c, (SELECT collegeid, SUM(enrollment) AS enrollment_total
                             FROM college_diversity cd
                             GROUP BY cd.collegeid) AS ce
            JOIN college_tuition ct ON ct.collegeid = ce.collegeid
            WHERE ce.collegeid = c.collegeid
            ORDER BY ce.enrollment_total DESC
            LIMIT %(Limit)s;
            """
            params = {'Limit':Limit}
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
        query_result_df = pd.DataFrame(diversity_query_results, columns=['college', 'state', 'Minorities Enrolled',
        'In State Tuition', 'Out Of State Tuition'])
        print(query_result_df)

    # Which schools have the highest percent stem and make the most in there early_career (allow user to choose state if they want)
    def career_query(self, Limit, state):
        if Limit.isdigit() and state:
            query = """
            SELECT cst.collegeid, c.state, cst.percent_stem, cs.early_career
            FROM college_students cst
            JOIN college c ON c.collegeid = cst.collegeid
            JOIN college_salary cs ON cs.collegeid = cst.collegeid
            WHERE cst.percent_stem IS NOT NULL
            AND c.state = %(state)s
            ORDER BY percent_stem DESC
            LIMIT %(Limit)s;
            """
            params = {'Limit':Limit, 'state': state }
            career_query_results = self.query_with_params(query,params)
        elif Limit.isdigit() and not state:
            query = """
            SELECT cst.collegeid, c.state, cst.percent_stem, cs.early_career
            FROM college_students cst
            JOIN college c ON c.collegeid = cst.collegeid
            JOIN college_salary cs ON cs.collegeid = cst.collegeid
            WHERE cst.percent_stem IS NOT NULL
            ORDER BY percent_stem DESC
            LIMIT %(Limit)s;
            """
            params = {'Limit':Limit}
            career_query_results = self.query_with_params(query, params)
        elif not Limit.isdigit() and state:
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
        query_result_df = pd.DataFrame(career_query_results, columns=['college', 'state', 'percent of student in stem',
        'early career salary'])
        print(query_result_df)

    #Which teams had a win percent over 80% in either basketball and football and enrolled over (let them choose)
    def team_query(self, win_percent, enrolled):
        if not win_percent:
            win_percent = .8
        if not enrolled:
            enrolled = 5000
        win_percent = float(win_percent)
        enrolled = float(enrolled)

        my_query = {'Win Percent': {'$gt' : win_percent}}
        basketball_dict = self.query_mongo('basketball', my_query)
        football_dict = self.query_mongo('football', my_query)
        teams_set = set()
        for i in basketball_dict:
            teams_set.add('%'+str(i['Team'])+'%')
        for i in football_dict:
            teams_set.add('%'+str(i['Team'])+'%')

        teams = list(teams_set)

        query = """
        SELECT c.collegeid, c.state, cs.enrolled, cs.type
        FROM college c, college_statistics cs
        WHERE c.collegeid = cs.collegeid
        AND c.collegeid LIKE ANY(%(teams)s)
        AND enrolled >= %(enrolled)s
        ORDER BY cs.enrolled;
        """
        params = {'teams': teams, 'enrolled':enrolled}
        query_results = self.query_with_params(query,params)
        query_result_df = pd.DataFrame(query_results, columns=['college', 'state', 'enrolled', 'public or private'])
        print(query_result_df)

    #Which state has the worst grad rate but the highest tuition
    def worst_grad_rate_query(self):
        query = """
            SELECT c.state, ROUND(AVG(CAST(cs.grad_rate AS NUMERIC)),2) AS grad_rate_avg, ROUND(AVG(CAST(cs.fulltime_undergrad AS NUMERIC)),2) AS fulltime_undergrad_AVG,
            ROUND(AVG(CAST(ct.in_state AS NUMERIC)),2) AS in_state_avg, ROUND(AVG(CAST(ct.out_of_state AS NUMERIC)),2) AS out_of_state_avg,
            ROUND(AVG(CAST(csa.making_a_difference AS NUMERIC)),2) AS making_a_difference_avg
            FROM college_students cs, college c, college_tuition ct, college_salary csa
            WHERE c.collegeid = cs.collegeid
            AND c.collegeid = ct.collegeid
            AND c.collegeid = csa.collegeid
            GROUP BY c.state
            ORDER BY grad_rate_avg ASC;
            """
        worst_grad_results = self.query_with_params(query)
        query_result_df = pd.DataFrame(worst_grad_results, columns=['State', 'Grad Rate AVG', 'Fulltime Undergrad AVG',
        'In State Tuition AVG', 'Out Of State Tuition AVG', 'Making A Difference AVG' ])
        print(query_result_df)

    #Do schools with the highest win percantage in both football and basketball have a lot of professors with phds and how many students are in stem
    def sport_query(self):
        my_query_basketball = {'$and' : [{ 'Power Rating': { '$gt' : .8}}, {'Playoff.Wins Cutoff': { '$gt' : 0}}]}
        my_query_football = {'$and': [{ '$expr' : { '$gt' : ["$Loss", "$Win"]} } , {'Offensive.Rank': { '$lt' : 10}}]}
        basketball_dict = self.query_mongo('basketball', my_query_basketball)
        football_dict = self.query_mongo('football', my_query_football)
        teams_set = set()
        for i in basketball_dict:
            teams_set.add('%'+str(i['Team'])+'%')
        for i in football_dict:
            teams_set.add('%'+str(i['Team'])+'%')

        teams = list(teams_set)

        query = """
        SELECT c.collegeid, c.state, cs.professor_with_phd, cst.percent_stem
        FROM college c, college_statistics cs, college_students cst
        WHERE c.collegeid = cs.collegeid
        AND c.collegeid = cst.collegeid
        AND c.collegeid LIKE ANY(%(teams)s);
        """
        params = {'teams': teams}
        query_results = self.query_with_params(query,params)
        query_result_df = pd.DataFrame(query_results, columns=['College', 'State', 'Professors with PhD', 'Percent of students in Stem'])
        print(query_result_df)
