# Structure of file
#1.) Flask Setup and HTML routes 
#2.) API lists of fields (???)
#3.) Routes that Depend on User inputs to filter data and render to Visualization

# 1.) Flask Set up and HTML Routes

import os

import pandas as pd
import numpy as np
import json

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


@app.route("/draft_data/<roster_size>/<num_teams>")
def draft_roster(roster_size, num_teams):
    roster_size = pd.to_numeric(roster_size).astype("int")
    num_teams = pd.to_numeric(num_teams).astype("int")
    draft_info2 = Draft.log_regression(2016,roster_size,num_teams,10)
    #draftData = json.loads(draft_info.to_json(orient='records'))
    #draftData = draft_info.to_json(orient='table')
    temp_data = draft_info2.to_dict('records')
    draftData2 = [dict(i) for i in temp_data]

    return json2html.convert(json = draftData2)    
    #return jsonify(draftData2)

@app.route("/matchup_data")
def matchup_data():
    
    matchup_info = Matchup.fantasy_matchup()
    matchupData = matchup_info.to_dict('dict')
    #temp = matchup_info.to_dict('records')
    #matchupData = [dict(i) for i in temp]
        
    return jsonify(matchupData)

@app.route("/matchup_data/<fteam1>/<fteam2>")
def matchup_data2(fteam1, fteam2):
    fteam1 = int(fteam1)
    fteam2 = int(fteam2)
    matchup_info2 = Matchup.fantasy_matchup(fteam1, fteam2)
    matchupData2 = matchup_info2.to_dict('dict')
    #temp = matchup_info.to_dict('records')
    #matchupData = [dict(i) for i in temp]
        
    return jsonify(matchupData2)


@app.route("/heatmap_data")
def heatmap_data():
    
    # Use Pandas to perform the sql query
    results_heat = db.session.query(Team_Loc).all()
    
    # Now get the needed data fields from the team location table.
    heat_data = []
    for result in results_heat:
        heat_dict = {}
        heat_dict["VENUEID"] = result.VENUEID
        heat_dict["NAME"] = result.NAME
        heat_dict["LATITUDE"] = result.LATITUDE
        heat_dict["LONGITUDE"] = result.LONGITUDE
        heat_dict["TEAM"] = result.TEAM
        heat_dict["POPULATION"] = result.POPULATION
        heat_dict["city_name"] = result.city_name
        heat_dict["Dist_to_Toronto"] = result.Dist_to_Toronto
        heat_dict["Dist_to_Dallas"] = result.Dist_to_Dallas
        heat_dict["Dist_to_SanAntonio"] = result.Dist_to_SanAntonio
        heat_dict["Dist_to_LosAngeles"] = result.Dist_to_LosAngeles
        heat_dict["Dist_to_Washington"] = result.Dist_to_Washington
        heat_dict["Dist_to_Indiana"] = result.Dist_to_Indiana
        heat_dict["Dist_to_Philadelphia"] = result.Dist_to_Philadelphia
        heat_dict["Dist_to_Chicago"] = result.Dist_to_Chicago
        heat_dict["Dist_to_Milwaukee"] = result.Dist_to_Milwaukee
        heat_dict["Dist_to_Minnesota"] = result.Dist_to_Minnesota
        heat_dict["Dist_to_Memphis"] = result.Dist_to_Memphis
        heat_dict["Dist_to_NewYork"] = result.Dist_to_NewYork
        heat_dict["Dist_to_Denver"] = result.Dist_to_Denver
        heat_dict["Dist_to_Atlanta"] = result.Dist_to_Atlanta
        heat_dict["Dist_to_Boston"] = result.Dist_to_Boston
        heat_dict["Dist_to_Phoenix"] = result.Dist_to_Phoenix
        heat_dict["Dist_to_Miami"] = result.Dist_to_Miami
        heat_dict["Dist_to_Sacramento"] = result.Dist_to_Sacramento
        heat_dict["Dist_to_Utah"] = result.Dist_to_Utah
        heat_dict["Dist_to_Cleveland"] = result.Dist_to_Cleveland
        heat_dict["Dist_to_GoldenState"] = result.Dist_to_GoldenState
        heat_dict["Dist_to_NewOrleans"] = result.Dist_to_NewOrleans
        heat_dict["Dist_to_Portland"] = result.Dist_to_Portland
        heat_dict["Dist_to_Charlotte"] = result.Dist_to_Charlotte
        heat_dict["Dist_to_Houston"] = result.Dist_to_Houston
        heat_dict["Dist_to_Detroit"] = result.Dist_to_Detroit
        heat_dict["Dist_to_OklahomaCity"] = result.Dist_to_OklahomaCity
        heat_dict["Dist_to_Orlando"] = result.Dist_to_Orlando
        heat_dict["Dist_to_Brooklyn"] = result.Dist_to_Brooklyn
        heat_data.append(heat_dict)
            
    return jsonify(heat_data)



@app.route("/heatmap_data2")
def heatmap_data2():
    
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


if __name__ == "__main__":
   app.run(debug=True)