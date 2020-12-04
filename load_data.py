import psycopg2
import psycopg2.extras
import utils
import numpy as np
import pymongo
from argparse import ArgumentParser
from collections import defaultdict


ag = ArgumentParser(description="Database configuration")
ag.add_argument("--host", dest='host', default='localhost')
args = ag.parse_args()
conn_string = f"host='{args.host}' dbname='final_project' user='project_user' password='goodGrades'"

class CollegeData:

    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # def setUp(self):
    #     with self.cursor as cursor:
    #         setup_queries = open('college-data.sql', 'r').read()
    #         cursor.execute(setup_queries)
    #         self.conn.commit()

    def check_connectivity(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM college LIMIT 1")
        records = cursor.fetchall()
        return len(records) == 1

    def query_with_params(self, query, params):
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

    def insert_college(self, college_df):
        tuples = [tuple(x) for x in college_df.to_numpy()]
        query = """ INSERT INTO college
        VALUES(%s,%s)"""
        self.execute_many(query, tuples)

    def insert_historical(self, historical_df):
        tuples = [tuple(x) for x in historical_df.to_numpy()]
        query = """ INSERT INTO historical_tuition
        VALUES(%s,%s,%s,%s)"""
        self.execute_many(query, tuples)

    def insert_diversity(self, diversity_df):
        tuples = [tuple(x) for x in diversity_df.to_numpy()]
        query = """ INSERT INTO college_diversity
        VALUES(%s,%s,%s)"""
        self.execute_many(query, tuples)

    def insert_salary(self, salary_df):
        tuples = [tuple(x) for x in salary_df.to_numpy()]
        query = """ INSERT INTO college_salary
        VALUES(%s,%s,%s,%s)"""
        self.execute_many(query, tuples)

    def insert_student(self, student_df):
        tuples = [tuple(x) for x in student_df.to_numpy()]
        query = """ INSERT INTO college_students
        VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        self.execute_many(query, tuples)

    def insert_statistic(self, statistic_df):
        tuples = [tuple(x) for x in statistic_df.to_numpy()]
        query = """ INSERT INTO college_statistics
        VALUES(%s,%s,%s,%s,%s,%s,%s)"""
        self.execute_many(query, tuples)

    def insert_tuition(self, tuition_df):
        tuples = [tuple(x) for x in tuition_df.to_numpy()]
        query = """ INSERT INTO college_tuition
        VALUES(%s,%s,%s,%s,%s,%s)"""
        self.execute_many(query, tuples)

if __name__ == '__main__':
    college = CollegeData(conn_string)

    college_df, student_df, statistic_df = utils.loaddata_college()
    college.insert_college(college_df)
    college.insert_student(student_df)
    college.insert_statistic(statistic_df)

    tuition_df = utils.loaddata_tuition()
    college.insert_tuition(tuition_df)

    historical_df = utils.loaddata_historical()
    college.insert_historical(historical_df)

    diversity_df = utils.loaddata_diversity()
    college.insert_diversity(diversity_df)

    salary_df = utils.loaddata_salary()
    college.insert_salary(salary_df)
