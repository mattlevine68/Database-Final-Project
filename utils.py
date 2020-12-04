import pandas as pd
import numpy as np

def loaddata_historical():
    historical_df = pd.read_csv("data/historical_tuition.csv")
    for i in historical_df.index:
        historical_df.at[i,'year'] = historical_df.at[i,'year'][:4]
    return historical_df

def loaddata_diversity():
    diversity_df = pd.read_csv("data/diversity_school.csv")
    diversity_df.drop(['total_enrollment', 'state'], axis=1, inplace=True)
    return diversity_df

def loaddata_college():
    # Put needed csv files in dataframes and clean data
    college_df = pd.read_csv("data/College_Data.csv")
    college_df.rename(columns={"Unnamed: 0": "collegeid"}, inplace=True)
    diversity_df = diversity_df = pd.read_csv("data/diversity_school.csv")
    diversity_df.rename(columns={"name": "collegeid"}, inplace=True)
    salary_df = pd.read_csv("data/salary_potential.csv")
    salary_df.rename(columns={"name": "collegeid"}, inplace=True)

    #All the colleges for college table
    final_df = pd.merge(diversity_df,  college_df, on='collegeid', how='left')
    final_df.drop_duplicates(subset=['collegeid'], inplace=True)
    final_df.dropna(subset=['collegeid'], inplace=True)
    final_df = final_df.reset_index(drop=True)
    college_final_df = final_df[['collegeid','state']]
    college_final_df = college_final_df.where(pd.notnull(college_final_df), None)

    #Data for college_students table
    student_final_df = college_df[['collegeid', 'Top10perc', 'Top25perc', 'F.Undergrad','P.Undergrad','Grad.Rate']]
    student_final_df = pd.merge(student_final_df,  salary_df, on='collegeid', how='left')
    student_final_df = student_final_df[['collegeid', 'Top10perc', 'Top25perc', 'F.Undergrad','P.Undergrad','Grad.Rate','stem_percent']]
    student_final_df = student_final_df.where(pd.notnull(student_final_df), None)
    #
    # #Data for college_statistics table
    statistics_final_df = college_df[['collegeid', 'Private', 'Apps', 'Accept', 'Enroll', 'PhD','Terminal']]
    statistics_final_df.Private.replace(to_replace=['Yes','No'], value=['Private', 'Public'],  inplace=True)

    return college_final_df, student_final_df, statistics_final_df

def loaddata_salary():
    salary_df = pd.read_csv("data/salary_potential.csv")
    salary_df.drop(['rank','state_name','stem_percent'], axis=1, inplace=True)
    return salary_df

def loaddata_tuition():
    tuition_df = pd.read_csv("data/tuition_cost.csv")
    tuition_df['year'] = None
    for i in tuition_df.index:
        tuition_df.at[i,'year'] = 2018
        tuition_df.at[i, 'degree_length'] = tuition_df.at[i, 'degree_length'][:1]
        if not tuition_df.at[i, 'degree_length'].isdigit():
            tuition_df.at[i, 'degree_length']  = None

    tuition_df = tuition_df[['name','year','degree_length','room_and_board','in_state_tuition', 'out_of_state_tuition']]
    tuition_df = tuition_df.where(pd.notnull(tuition_df), None)

    return tuition_df

def loaddata_sports():
    pass
