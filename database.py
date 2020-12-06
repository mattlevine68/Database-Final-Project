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

    def commit_execute(self, query, params):
        self.cursor.execute(query, params)
        self.conn.commit()

    def execute_many(self, query, params):
        self.cursor.executemany(query, params)
        self.conn.commit()

    # Which school and state has the most diversity and whats the tuition tuition
    def diversity_query(self):
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
        query_result_df = pd.DataFrame(diversity_query_results, columns=['college', 'state', 'Minorities Enrolled', 'In State Tuition', 'Out Of State Tuition'])
        print(query_result_df)

    # Which schools have the highest percent stem and make the most in there early_career (allow user to choose state if they want)
    def career_query(self, state):
        pass

    #Which teams had a win percent over 80% in both basketball and football (regardless of year but give the option) and enrolled over (let them choose)
    def team_query(self, win_percent, enrolled):
        pass

    #Which state has the worst grad rate but the highest tuition
    def worst_grad_rate_query(self):
        pass

    #Do schools with the highest win percantage in both football and basketball have a lot of professors with phds and how many students are in stem
    def sport_query(self):
        pass



#SELECT cs.collegeid,co.state,  cs.grad_rate, c.degree_length, c.out_of_state, css.type  FROM college_students cs
# JOIN college_tuition c ON cs.collegeid = c.collegeid
# JOIN college co ON co.collegeid = cs.collegeid
# JOIN college_statistics css ON css.collegeid =  cs.collegeid
# ORDER BY grad_rate ASC
# LIMIT 10;
