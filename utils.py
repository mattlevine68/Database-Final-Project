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
    diversity_df.rename(columns={"name": "collegeid"}, inplace=True)
    salary_df = pd.read_csv("data/salary_potential.csv")
    salary_df.rename(columns={"name": "collegeid"}, inplace=True)

    final_df = pd.merge(diversity_df,  college_df, on='collegeid', how='left')
    final_df.drop_duplicates(subset=['collegeid'], inplace=True)
    final_df.dropna(subset=['collegeid'], inplace=True)
    final_df = final_df.reset_index(drop=True)
    college_final_df = final_df[['collegeid','state','Private','Apps','Accept','total_enrollment','PhD','Terminal']]
    college_final_df = college_final_df.where(pd.notnull(college_final_df), None)

    student_final_df = final_df[['collegeid', 'Top10perc', 'Top25perc', 'F.Undergrad','P.Undergrad','Grad.Rate']]
    student_final_df = pd.merge(student_final_df,  salary_df, on='collegeid', how='left')
    student_final_df = student_final_df[['collegeid', 'Top10perc', 'Top25perc', 'F.Undergrad','P.Undergrad','Grad.Rate','stem_percent']]
    student_final_df = student_final_df.where(pd.notnull(student_final_df), None)

    return college_final_df, student_final_df

def loaddata_salary():
    salary_df = pd.read_csv("data/salary_potential.csv")
    salary_df.drop(['rank','state_name','stem_percent'], axis=1, inplace=True)
    return salary_df

def loaddata_sports():
    
