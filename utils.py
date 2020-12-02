import pandas as pd
import numpy as np

def loaddata():
    college_df = pd.read_csv("data/College_Data.csv")
    college_df.rename(columns={"Unnamed: 0": "collegeid"}, inplace=True)
    diversity_df = pd.read_csv("data/diversity_school.csv")
    salary_df = pd.read_csv("data/salary_potential.csv")
    tuiton_df = pd.read_csv("data/tuition_cost.csv")
    historical_df = pd.read_csv("data/historical_tuition.csv")

def loaddata_historical():
    historical_df = pd.read_csv("data/historical_tuition.csv")
    for i in historical_df.index:
        historical_df.at[i,'year'] = historical_df.at[i,'year'][:4]
    return historical_df

def loaddata_diversity():
    diversity_df = pd.read_csv("data/diversity_school.csv")
    diversity_df.drop(['total_enrollment', 'state'], axis=1, inplace=True)
    return diversity_df

#Gotta figure out tables cause I'm fucked
def loaddata_college():
    college_df = pd.read_csv("data/College_Data.csv")
    college_df.rename(columns={"Unnamed: 0": "collegeid"}, inplace=True)

    diversity_df = diversity_df = pd.read_csv("data/diversity_school.csv")
    diversity_df.drop(['total_enrollment', 'state'], axis=1, inplace=True)

    college_state_diverse = diversity_df.groupby("name", as_index=False)
    #final_df = pd.merge(college_state_diverse,  diversity_df, on=['name','collegeid'], how='left')

    print(college_state_diverse.head())


    return 0,0

    # student_df = pd.read_csv("data/College_Data.csv")
    # student_df.rename(columns={"Unnamed: 0": "collegeid"}, inplace=True)

def loaddata_salary():
    salary_df = pd.read_csv("data/salary_potential.csv")
    salary_df.drop(['rank','state_name','stem_percent'], axis=1, inplace=True)
    return salary_df
