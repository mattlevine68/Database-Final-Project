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

def loaddata_basketball():
    basketball_df = pd.read_csv("data/cbb.csv")
    rst = []
    basketball_df = basketball_df.astype({'YEAR': 'object','W':'object','G':'object'})
    for i in basketball_df.index:
        data = {
            '_id': i,
            'Team' : basketball_df.loc[i]['TEAM'],
            'Year' : basketball_df.loc[i]['YEAR'],
            'Conference' : basketball_df.loc[i]['CONF'],
            'Games' : basketball_df.loc[i]['G'],
            'Wins'  : basketball_df.loc[i]['W'],
            'Win Percent': basketball_df.loc[i]['W']/basketball_df.loc[i]['G'],
            'Power Rating': basketball_df.loc[i]['BARTHAG'],
            'Offensive' : {
                'Efficency' : basketball_df.loc[i]['ADJOE'],
                'Field Goals' : basketball_df.loc[i]['EFG_O'],
                'Steals' : basketball_df.loc[i]['TORD'],
                'Rebounds' : basketball_df.loc[i]['ORB'],
                'Free Throws' : basketball_df.loc[i]['FTR'],
                'Two Pointers' : basketball_df.loc[i]['2P_O'],
                'Three Pointers' :basketball_df.loc[i]['3P_O']
            },
            'Defensive' : {
                'Efficency' : basketball_df.loc[i]['ADJDE'],
                'Field Goals Allowed' : basketball_df.loc[i]['EFG_D'],
                'Turnovers' : basketball_df.loc[i]['TOR'],
                'Rebounds Allowed' : basketball_df.loc[i]['DRB'],
                'Free Throws Allowed' : basketball_df.loc[i]['FTRD'],
                'Two Pointers Allowed' : basketball_df.loc[i]['2P_D'],
                'Three Pointers Allowed' : basketball_df.loc[i]['3P_D'],
                'Tempo' : basketball_df.loc[i]['ADJ_T']
            },
            'Playoff' : {
                'Wins Cutoff'  :  basketball_df.loc[i]['WAB'],
                'Postseason Round':  basketball_df.loc[i]['POSTSEASON'],
                'Seed': basketball_df.loc[i]['SEED']
            }
        }
        rst.append(data)
    return rst

def loaddata_football():
    football_df = pd.read_csv("data/CFB2019.csv")
    football_df['Conference'] = football_df['Team']

    new = football_df['Win-Loss'].str.split('-', n=1, expand=True)
    football_df['Win'] = new[0]
    football_df['Loss'] = new[1]
    football_df.drop(columns=['Win-Loss'],inplace=True)
    football_df = football_df.astype(object)
    rst =  []
    for i in football_df.index:
        index = football_df.at[i,'Conference'].index('(')
        football_df.at[i,'Conference'] = football_df.at[i,'Conference'][index+1:-1]
        football_df.at[i,'Team'] = football_df.at[i,'Team'][:index-1]
        if football_df.at[i,'Team'][-1] == '.':
            football_df.at[i,'Team'] = football_df.at[i,'Team'][:index-1][:-1]
        data = {
            '_id' : i,
            'Team' : football_df.at[i,'Team'],
            'Conference' : football_df.at[i,'Conference'],
            'Win' : int(football_df.at[i,'Win']),
            'Loss' : int(football_df.at[i,'Loss']),
            'Win Percent' : int(football_df.at[i,'Win'])/(int(football_df.at[i,'Loss']) + int(football_df.at[i,'Win'])),
            'Offensive' : {
                'Rank' : football_df.at[i,'Off Rank'],
                'Plays' : football_df.at[i,'Off Plays'],
                'Yards' : football_df.at[i,'Off Yards'],
                'Yards per Play' : football_df.at[i,'Off Yards/Play'],
                'Touchdowns' : football_df.at[i,'Off TDs'],
                'Yards per Game' : football_df.at[i,'Off Yards per Game'],
                'First Down Stats' : {
                    'Rank' : football_df.at[i,'First Down Rank'],
                    'Runs' : football_df.at[i,'First Down Runs'],
                    'Passing' : football_df.at[i,'First Down Passes'],
                    'Penalties' : football_df.at[i,'First Down Penalties'],
                    'First Downs' : football_df.at[i,'First Downs']
                },
                'Fourth Down Stats' : {
                    'Rank' : football_df.at[i,'4th Down Rank'],
                    'Attempts' : football_df.at[i,'4th Attempts'],
                    'Conversions' : football_df.at[i,'4th Conversions'],
                    'Percent Made' : football_df.at[i,'4th Percent']
                },
                'Passing' : {
                    'Rank' : football_df.at[i,'Passing Off Rank'],
                    'Attempts' : football_df.at[i,'Pass Attempts'],
                    'Completions' : football_df.at[i,'Pass Completions'],
                    'Interceptions' : football_df.at[i,'Interceptions Thrown.x'],
                    'Total Yards' : football_df.at[i,'Pass Yards'],
                    'Yards per Completion' : football_df.at[i,'Yards/Completion'],
                    'Touchdowns' : football_df.at[i,'Pass Touchdowns'],
                    'Yards per Game' : football_df.at[i,'Pass Yards Per Game'],
                },
                'Redzone' : {
                    'Rank' : football_df.at[i,'Redzone Off Rank'],
                    'Attempts' : football_df.at[i,'Redzone Attempts'],
                    'Rush Touchdowns' : football_df.at[i,'Redzone Rush TD'],
                    'Pass Touchdowns' : football_df.at[i,'Redzone Pass TD'],
                    'Field Goals' : football_df.at[i,'Redzone Field Goals Made'],
                    'Times Scored' : football_df.at[i,'Redzone Scores'],
                    'Points' : football_df.at[i,'Redzone Points'],
                },
                'Rushing' : {
                    'Rank' : football_df.at[i,'Rushing Off Rank'],
                    'Attempts' : football_df.at[i,'Rush Attempts'],
                    'Rush Yard Total' : football_df.at[i,'Rush Yds'],
                    'Yards Per Rush' : football_df.at[i,'Yards/Rush'],
                    'Touchdowns' : football_df.at[i,'Rushing TD'],
                    'Yards Per Game' : football_df.at[i,'Rushing Yards per Game']
                }
            },
            'Defensive' : {
                'Rank' : football_df.at[i,'Def Rank'],
                'Plays' : football_df.at[i,'Def Plays'],
                'Yards Allowed' : football_df.at[i,'Yards Allowed'],
                'Yards Per Play Allowed' : football_df.at[i,'Yards/Play Allowed'],
                'Off Touchdown Allowed' : football_df.at[i,'Off TDs Allowed'],
                'Total Touchdown Allowed' : football_df.at[i,'Total TDs Allowed'],
                'Yards Per Game Allowed' : football_df.at[i,'Yards Per Game Allowed'],
                'First Down Stats' : {
                    'Rank' : football_df.at[i,'First Down Def Rank'],
                    'Runs' : football_df.at[i,'Opp First Down Runs'],
                    'Passing' : football_df.at[i,'Opp First Down Passes'],
                    'Penalties' : football_df.at[i,'Opp First Down Penalties'],
                    'First Downs' : football_df.at[i,'Opp First Downs']
                },
                'Fourth Down Stats' : {
                    'Rank' : football_df.at[i,'4rd Down Def Rank'],
                    'Attempts' : football_df.at[i,'Opp 4th Attempt'],
                    'Conversions' : football_df.at[i,'Opp 4th Conversion'],
                    'Percent Made' : football_df.at[i,'4th Percent']
                },
                'Passing' : {
                    'Rank' : football_df.at[i,'Pass Def Rank'],
                    'Attempts' : football_df.at[i,'Opp Pass Attempts'],
                    'Completions' : football_df.at[i,'Opp Completions Allowed'],
                    'Total Yards' : football_df.at[i,'Opp Pass Yds Allowed'],
                    'Yards per Completion' : football_df.at[i,'Yards/Completion Allowed'],
                    'Yards per Attempt' : football_df.at[i,'Yards/Attempt Allowed'],
                    'Touchdowns' : football_df.at[i,'Opp Pass TDs Allowed'],
                    'Yards per Game' : football_df.at[i,'Pass Yards Per Game Allowed']
                },
                'Redzone' : {
                    'Rank' : football_df.at[i,'Redzone Def Rank'],
                    'Attempts' : football_df.at[i,'Opp Redzone Attempts'],
                    'Rush Touchdowns Allowed' : football_df.at[i,'Opp Redzone Rush TD Allowed'],
                    'Pass Touchdowns Allowed' : football_df.at[i,'Opp Redzone Pass Touchdowns Allowed'],
                    'Field Goals' : football_df.at[i,'Opp Redzone Field Goals Made'],
                    'Times Oppenent Scored' : football_df.at[i,'Opp Redzone Scores'],
                    'Points Allowed' : football_df.at[i,'Redzone Points Allowed'],
                },
                'Rushing' : {
                    'Rank' : football_df.at[i,'Rushing Def Rank'],
                    'Attempts' : football_df.at[i,'Opp Rush Attempts'],
                    'Allowed' : football_df.at[i,'Opp Rush Yards Alloweed'],
                    'Yards Per Rush' : football_df.at[i,'Yds/Rush Allowed'],
                    'Touchdowns' : football_df.at[i,'Opp Rush Touchdowns Allowed'],
                    'Yards Per Game' : football_df.at[i,'Rush Yards Per Game Allowed']
                }
            },
            'Special Teams' : {
                'Offensive' : {
                    'Kickoff' : {
                        'Rank' : football_df.at[i,'Kickoff Return Rank'],
                        'Return Attemps' : football_df.at[i,'Kickoffs Returned'],
                        'Return Yards' : football_df.at[i,'Kickoff Return Yards'],
                        'Touchdowns' : football_df.at[i,'Kickoff Return Touchdowns'],
                        'Average Return Yards' : football_df.at[i,'Avg Yard per Kickoff Return']
                    },
                    'Punts' : {
                        'Rank' : football_df.at[i,'Punt Return Rank'],
                        'Total Returns' : football_df.at[i,'Punt Returns'],
                        'Total Return Yards' : football_df.at[i,'Net Punt Return Yards'],
                        'Touchdowns' : football_df.at[i,'Punt Return Touchdowns'],
                        'Average Return Yards' : football_df.at[i,'Avg Yards Per Punt Return']
                    }
                },
                'Defensive' : {
                    'Kickoff' : {
                        'Rank' : football_df.at[i,'Kickoff Return Def Rank'],
                        'Opponents Return Attemps' : football_df.at[i,'Opp Kickoff Returns'],
                        'Touchbacks' : football_df.at[i,'Kickoff Touchbacks'],
                        'Allowed Return Yards' : football_df.at[i,'Opponent Kickoff Return Yards'],
                        'Allowed Touchdowns' : football_df.at[i,'Opp Kickoff Return Touchdowns Allowed'],
                        'Average Return Yards' : football_df.at[i,'Avg Yards per Kickoff Return Allowed']
                    },
                    'Punts' : {
                        'Rank' : football_df.at[i,'Punt Return Def Rank'],
                        'Total Returns' : football_df.at[i,'Opp Punt Returns'],
                        'Total Return Yards' : football_df.at[i,'Opp Net Punt Return Yards'],
                        'Touchdowns' : football_df.at[i,'Opp Punt Return Touchdowns Allowed'],
                        'Average Return Yards' : football_df.at[i,'Avg Yards Allowed per Punt Return']
                    }
                }
            },
            'Penalties' : {
                'Rank' : football_df.at[i,'Penalty Rank'],
                'Total Amount' : football_df.at[i,'Penalties'],
                'Total Yards Lost' : football_df.at[i,'Penalty Yards'],
                'Yards Per Game' : football_df.at[i,'Penalty Yards Per Game']
            }

        }
        rst.append(data)


    return rst


# Sack Rank,
# Sacks,
# Sack Yards,
# Average Sacks per Game,
# Scoring Def Rank,
# Touchdowns Allowed,
# Opponent Extra Points,
# 2 Point Conversions Allowed,
# Opp Deflected Extra Points,
# Opp Feild Goals Made,
# Opp Safety,
# Points Allowed,
# Avg Points per Game Allowed,
# Scoring Off Rank,
# Touchdowns,
# PAT,
# 2 Point Conversions,
# Defensive Points,
# Feild Goals,
# Safety,
# Total Points,
# Points Per Game,
# Tackle for Loss Rank,
# Solo Tackle For Loss,
# Assist Tackle For Loss,
# Tackle for Loss Yards,
# Total Tackle For Loss,
# Tackle For Loss Per Game,
# 3rd Down Rank,
# 3rd Attempts,
# 3rd Conversions,
# 3rd Percent,
# Time of Possession Rank,
# Time of Possession,
# Average Time of Possession per Game,
# Turnover Rank,
# Fumbles Recovered,
# Opponents Intercepted,
# Turnovers Gain,
# Fumbles Lost,
# Interceptions Thrown.y,
# Turnovers Lost,
# Turnover Margin,
# Avg Turnover Margin per Game
