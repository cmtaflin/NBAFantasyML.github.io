# Structure of file
#1.) Flask Setup and HTML routes 
#2.) API lists of fields (???)
#3.) Routes that Depend on User inputs to filter data and render to Visualization

# 1.) Flask Set up and HTML Routes

import os

import pandas as pd
import numpy as np
import json
from json2html import *

#commenting out mySQL reference since we are using SQLite
#import pymysql
#pymysql.install_as_MySQLdb()

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine , func
import sqlite3

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

import Draft
import Matchup
import json_geojson

#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/NBA_Data.sqlite"
db = SQLAlchemy(app)

# engine = create_engine("sqlite:///db/NBAfantasyML.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)
session = Session(db.engine)


# Save references to each table
Team_Loc = Base.classes.Team_Locations
Teams = Base.classes.All_Teams
Fantasy_Draft = Base.classes.NBA_Fantasy_Draft
Season1617 = Base.classes.season_2016_2017
Season1718 = Base.classes.season_2017_2018
Playerstats = Base.classes.playerstats_boxscore



@app.route("/")
def index():
    
    return render_template("index.html")


@app.route("/heatmap")
def heatmap():
    
    
    return render_template("heatmap.html")


@app.route("/playerdraft")
def playerdraft():
    
    return render_template("playerdraft.html")


@app.route("/fantasymatch")
def fantasymatch():
    
    return render_template("fantasymatch.html")


@app.route("/pointsposition")
def pointsposition():
    
    return render_template("pointsposition.html")

@app.route("/draft_data")
def draft_data():
    
    draft_info = Draft.log_regression(2016,13,10,10)
    #draftData = json.loads(draft_info.to_json(orient='records'))
    #draftData = draft_info.to_json(orient='table')
    temp = draft_info.to_dict('records')
    draftData = [dict(i) for i in temp]
        
    return jsonify(draftData)

@app.route("/json_draft_data/<roster_size>/<num_teams>")
def draft_roster(roster_size, num_teams):
    roster_size = pd.to_numeric(roster_size).astype("int")
    num_teams = pd.to_numeric(num_teams).astype("int")
    draft_info2 = Draft.log_regression(2016,roster_size,num_teams,10)
    #draftData = json.loads(draft_info.to_json(orient='records'))
    #draftData = draft_info.to_json(orient='table')
    #draft_info2 = draft_info2[['Rank','Player', 'zFT', 'z3P', 'zPTS', 'zREB', 'zAST', 'zSTL', 'zBLK', 'zTOV', 'zAVG']]
    #draft_info2 = draft_info2.round({'zFT': 2, 'z3P': 2, 'zPTS': 2, 'zREB': 2, 'zAST': 2, 'zSTL': 2, 'zBLK': 2, 'zTOV': 2, 'zAVG': 2})
    temp_data = draft_info2.to_dict('records')
    draftData2 = [dict(i) for i in temp_data]
    return jsonify(draftData2)

@app.route("/draft_data/<roster_size>/<num_teams>")
def draft_roster1(roster_size, num_teams):
    roster_size = pd.to_numeric(roster_size).astype("int")
    num_teams = pd.to_numeric(num_teams).astype("int")
    draft_info2 = Draft.log_regression(2016,roster_size,num_teams,10)
    #draftData = json.loads(draft_info.to_json(orient='records'))
    #draftData = draft_info.to_json(orient='table')
    draft_info2 = draft_info2[['Rank','Player', 'zFT', 'z3P', 'zPTS', 'zREB', 'zAST', 'zSTL', 'zBLK', 'zTOV', 'zAVG']]
    draft_info2 = draft_info2.round({'zFT': 2, 'z3P': 2, 'zPTS': 2, 'zREB': 2, 'zAST': 2, 'zSTL': 2, 'zBLK': 2, 'zTOV': 2, 'zAVG': 2})
    temp_data = draft_info2.to_dict('records')
    draftData2 = [dict(i) for i in temp_data]
    return json2html.convert(json = draftData2) 
    #return jsonify(draftData2)

@app.route("/matchup_data")
def matchup_data():
        
    matchup_info = Matchup.fantasy_matchup()
    matchup_info = matchup_info.round({"team1": 2, "team2": 2})
    matchupData = matchup_info.to_dict('dict')
        
    return jsonify(matchupData)

@app.route("/matchup_data/<fteam1>/<fteam2>")
def matchup_data2(fteam1, fteam2):
    
    fteam1 = int(fteam1)
    fteam2 = int(fteam2)
    matchup_info2 = Matchup.fantasy_matchup(fteam1, fteam2)
    matchup_info2 = matchup_info2.round({"team1": 2, "team2": 2})
    matchupData2 = matchup_info2.to_dict('dict')
        
    return jsonify(matchupData2)

@app.route("/getids/<name>")
def get_ids(name):
    ids = Matchup.get_ids(name)
    id_1 = ids.to_dict('dict')
    
    return jsonify(id_1)


@app.route("/heatmap_data")
def heatmap_data():
    
    # Use Pandas to perform the sql query
    results_heat2 = db.session.query(Team_Loc).statement
    df = pd.read_sql_query(results_heat2, db.session.bind)
    
    #generate list of columns to include
    properties = list(df.columns.values)
    
    #assign equivalent columns for the latitude and longitude
    lat = 'LATITUDE'
    lon = 'LONGITUDE'
    
    geojson = json_geojson.to_geojson(df, properties, lat, lon)
            
    return jsonify(geojson)

@app.route("/boxscore_data")
def boxscore_data():
    
    # Use Pandas to perform the sql query for boxscore data
    results_playerstat = db.session.query(Playerstats).statement
    df = pd.read_sql_query(results_playerstat, db.session.bind)
    
    # drop player data where they did not play
    df = df[df.dnp == ""]
    
    # group by gameId and start processing total box scores to come up with totals
    game_data = df.groupby("gameId")
    
    tot_game_points = game_data["points"].sum()
    tot_game_steals = game_data["steals"].sum()
    tot_game_Reb = game_data["totReb"].sum()
    tot_game_assists = game_data["assists"].sum()
    
    # get the unique list of games/city combinations
    venue_gameId = game_data["city_name"].first()
    
    # place data into dataframes and merge
    df_tot_points = pd.DataFrame(tot_game_points)
    df_tot_steals = pd.DataFrame(tot_game_steals)
    df_tot_Reb = pd.DataFrame(tot_game_Reb)
    df_tot_assists = pd.DataFrame(tot_game_assists)
    df_city_game = pd.DataFrame(venue_gameId)
    
    # merge dataframes into one
    game_info = pd.merge(pd.merge(pd.merge(pd.merge(df_tot_points, df_tot_steals, on="gameId"), df_tot_Reb, on="gameId"), 
                                  df_city_game, on="gameId"), df_tot_assists, on="gameId")
    
    # now group by city to get stats per location
    group_by_city = game_info.groupby("city_name")
    ppg = group_by_city["points"].mean().round(2)
    spg = group_by_city["steals"].mean().round(2)
    rpg = group_by_city["totReb"].mean().round(2)
    apg = group_by_city["assists"].mean().round(2)
    
    # create dataframes for the data above
    ppg_df = pd.DataFrame(ppg)
    spg_df = pd.DataFrame(spg)
    rpg_df = pd.DataFrame(rpg)
    apg_df = pd.DataFrame(apg)
    
    # bring in team location data table so we can make a geojson
    results_Loc = db.session.query(Team_Loc).statement
    Loc_df = pd.read_sql_query(results_Loc, db.session.bind)
    
    # create final dataframe by merging the boxscore data into the location table
    Loc_data = pd.merge(pd.merge(pd.merge(pd.merge(Loc_df, ppg_df, on="city_name"), spg_df, on="city_name"), 
                     rpg_df, on="city_name"), apg_df, on="city_name")

    
    #generate list of columns to include in final geojson
    properties_box = list(Loc_data.columns.values)
    
    #assign equivalent columns for the latitude and longitude
    lat = 'LATITUDE'
    lon = 'LONGITUDE'
    
    geojson_boxscore = json_geojson.to_geojson(Loc_data, properties_box, lat, lon)
            
    return jsonify(geojson_boxscore)


#testing out the NBA graphs
@app.route("/pointsposition_test")
def pointsposition_test():
    
    
    return render_template("pointsposition_test.html")


@app.route("/NBA-graph/center")
def graph_center():
    
    
    return render_template("/NBA-graph/center.html")


@app.route("/NBA-graph/powerforward")
def graph_powerforward():
    
    
    return render_template("/NBA-graph/powerforward.html")


@app.route("/NBA-graph/smallforward")
def graph_smallforward():
    
    
    return render_template("/NBA-graph/smallforward.html")


@app.route("/NBA-graph/shootingguard")
def graph_shootingguard():
    
    
    return render_template("/NBA-graph/shootingguard.html")


@app.route("/NBA-graph/pointguard")
def graph_pointguard():
    
    
    return render_template("/NBA-graph/pointguard.html")

if __name__ == "__main__":
   app.run(debug=True)