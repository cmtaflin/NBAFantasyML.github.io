# Dependencies and Setup
import json
import pandas as pd
import numpy as np
import requests
import numpy as py
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float, Date
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, inspect, func, distinct
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import sqlite3
from sqlite3 import Error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

#setup the database connection
#def enginetest():
    #engine = create_engine("sqlite:///db/NBA_Data.sqlite")
    
def conntest():
    engine = create_engine("sqlite:///db/NBA_Data.sqlite")
    conn = engine.connect()
    return conn

def week_games(teamId = 1610612740, personId = 201950, startday = 20190204):
    #Bring in data from internet as object then convert ot Json and count number of games
    # REQUEST
    schedule_response_obj=requests.get("http://data.nba.net/prod/v1/2018/schedule.json")
    schedule_response=schedule_response_obj.json()

    ###   Collect Elements for URL, append List, create DataFrame, DF_exclude games not played  ###
    # Bring in Game Id and GameData ("startDataEastern") elements from NBA Schedule later used to create box_score URL
    # Get elements
    NBA_Schedule=[]
    for item in schedule_response["league"]["standard"]:
        item_dict={}
        item_dict["gameId"]=item["gameId"]
        item_dict["hTeam_Id"]=item["hTeam"]["teamId"]
        item_dict["aTeam_Id"]=item["vTeam"]["teamId"]
        item_dict["startDateEastern"]=item["startDateEastern"]
        item_dict["statusNum"]=item["statusNum"]
    # Append List
        NBA_Schedule.append({"gameId":item_dict["gameId"],
                             "hTeam_Id":item_dict["hTeam_Id"],
                             "aTeam_Id":item_dict["aTeam_Id"],
                             "startdateeastern":item_dict["startDateEastern"],
                             "statusnum":item_dict["statusNum"]})
    # Convert NBA_Schedule=[] list to DataFrame and modify Datatypes
    NBA_Schedule_DF_initial=pd.DataFrame(NBA_Schedule)
    NBA_Schedule_DF_initial["gameId"]=NBA_Schedule_DF_initial["gameId"].astype(int)
    NBA_Schedule_DF_initial["hTeam_Id"]=NBA_Schedule_DF_initial["hTeam_Id"].astype(int)
    NBA_Schedule_DF_initial["aTeam_Id"]=NBA_Schedule_DF_initial["aTeam_Id"].astype(int)
    NBA_Schedule_DF_initial["startdateeastern"]=NBA_Schedule_DF_initial["startdateeastern"].astype(int)
    NBA_Schedule_DF_initial["statusnum"]=NBA_Schedule_DF_initial["statusnum"].astype(int)
    
    next_week_days = range(startday,startday+7)
    next_week = NBA_Schedule_DF_initial.loc[NBA_Schedule_DF_initial["startdateeastern"].isin(next_week_days),:].reset_index()
    
    away_games = next_week[(next_week.aTeam_Id == teamId)]
    away_games["versus"] = away_games["hTeam_Id"]
    home_games = next_week[(next_week.hTeam_Id == teamId)]
    home_games["versus"] = home_games["aTeam_Id"]

    games_df = pd.concat([home_games, away_games], axis = 0)
    
    return games_df;

def linear_reg(personId = 201950, startday = 20190204):
    
    conn = conntest()
    
    # games so far this season
    df = pd.read_sql('select * from playerstats_boxscore', conn)
    
    # versus team stats
    vs_team = pd.read_sql('select * from adv_team_stats_2018_2019', conn)
    vs_team = vs_team.rename(columns={"teamid": "versus"})
    
    # take in one player
    train = df[df.personId == personId]
    train = train[train.dnp == ""].reset_index()
   
    train = pd.merge(vs_team, train, on="versus", how="inner")

    # categories
    points = ["fgm", "fga", "fgp", "ftm", "fta", "ftp", "tpm", "tpa", "tpp", "min", \
              'def_rating', 'pace', 'op_fgm', 'op_fga', 'op_fgp', 'op_tpm', 'op_tpa', \
              'op_tpp', 'op_ftm', 'op_fta', 'op_ftp', 'op_pFoulsDrawn', 'op_points']
    assists = ["min", 'pace']
    rebounds = ["offReb", "defReb", 'offRebP', 'defRebP', 'totRebP', 'pace', 'op_offReb', 'op_defReb', 'op_totReb']
    steals = ['min', 'turnover_p', 'pace', 'op_steals']
    turnovers = ['min', 'pace', 'op_turnovers']
    blocks = ['min', 'pace', 'op_blocks', 'op_blocksAttempt'] 
    threes = ["tpa", "tpp", 'min', 'op_tpm', 'op_tpa', 'op_tpp']
    field_goals = ['fga', 'fgp', 'min', 'def_rating', 'pace', 'op_fgm', 'op_fgp', 'op_tpm', 'op_tpa', 'op_tpp', 'op_points']
    fg_attempts = ['fgm', 'min', 'pace', 'op_fga', 'op_tpa']
    free_throws = ['fta', 'ftp', 'min', 'pace', 'op_ftm', 'op_fta', 'op_ftp', 'op_pFoulsDrawn']
    ft_attempts = ['ftm', 'ftp', 'min', 'pace', 'op_fta', 'op_pFoulsDrawn']

    categories = ["points", "assists", "totReb", "steals", "turnovers", "blocks", "tpm", "fgm", "fga", "ftm", "fta"]
    training = [points, assists, rebounds, steals, turnovers, blocks, threes, field_goals, fg_attempts, free_throws, ft_attempts]

    # next week games
    next_week = week_games(train["teamId"][0], personId, startday)
    next_week = pd.merge(vs_team, next_week, on="versus", how="inner")
    
    game_count=len(next_week)
    current_season_stats = pd.read_sql('select * from season_2018_2019', conn)
    this_season = current_season_stats[current_season_stats.personId == 201950] 
    this_season["fgp"] = this_season["fgp"]*100
    this_season["tpp"] = this_season["tpp"]*100
    this_season["ftp"] = this_season["ftp"]*100
    
    this_season = this_season.append([this_season]*(game_count-1),ignore_index=True)
    next_week = pd.concat([next_week, this_season], axis = 1)
    
    #next_week = train[:len(week_games(train["teamId"][0], personId, startday))]
    
    for x in range(11):
        X = train[training[x]]
        y = train[categories[x]].values.reshape(-1, 1)

        # Use train_test_split to create training and testing data
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

        # Create the model using LinearRegression
        model = LinearRegression()

        # Fit the model to the training data and calculate the scores for the training and testing data
        model.fit(X_train, y_train)
        training_score = model.score(X_train, y_train)
        testing_score = model.score(X_test, y_test)

        #print(f"Training Score: {training_score}")
        #print(f"Testing Score: {testing_score}")

        test = next_week[training[x]]
        prediction = model.predict(test)
        next_week[categories[x]] = prediction
    
    # predicted stats for next week
    weekly_prediction = next_week[categories].sum()
    weekly_prediction["fgp"] = weekly_prediction["fgm"] / weekly_prediction["fga"]
    weekly_prediction["ftp"] = weekly_prediction["ftm"] / weekly_prediction["fta"]

    return weekly_prediction.to_frame();


# def fantasy_matchup(team1_id = 7110302001, team2_id = 7110302002, startday = 20190204):
def get_ids(name):
    conn = conntest()
    get_team_id = pd.read_sql(f"select DISTINCT Fantasy_Team_ID from fantasy_league where Fantasy_Team_Name='{name}'", conn)
    return get_team_id


def fantasy_matchup(team1_id, team2_id, startday = 20190204):
    
    conn = conntest()
    
    # pull in data for 2 teams
    df = pd.read_sql('select * from fantasy_league', conn)
    team1 = df[df.Fantasy_Team_ID == team1_id].reset_index()
    team2 = df[df.Fantasy_Team_ID == team2_id].reset_index()
    
    # run lin_reg for each player
    total1 = pd.DataFrame()
    for x in range(0,len(team1)):
        total1 = pd.concat([total1, linear_reg(team1['personid'][x], startday)], axis = 1)
    sum1 = np.sum(total1, axis=1).to_frame().rename(columns={0: "team1"})

    total2 = pd.DataFrame()
    for x in range(0,len(team2)):
        total2 = pd.concat([total2, linear_reg(team2['personid'][x], startday)], axis = 1)
    sum2 = np.sum(total2, axis=1).to_frame().rename(columns={0: "team2"})
    
    matchup = pd.concat([sum1, sum2], axis = 1)
    
    matchup["team1"]["ftp"] = matchup["team1"]["ftm"] / matchup["team1"]["fta"]
    matchup["team1"]["fgp"] = matchup["team1"]["fgm"] / matchup["team1"]["fga"]
    matchup["team2"]["ftp"] = matchup["team2"]["ftm"] / matchup["team2"]["fta"]
    matchup["team2"]["fgp"] = matchup["team2"]["fgm"] / matchup["team2"]["fga"]
    
    return matchup;