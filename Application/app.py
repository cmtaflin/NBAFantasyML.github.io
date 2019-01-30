# Structure of file
#1.) Flask Setup and HTML routes 
#2.) API lists of fields (Happiness data, Country, Region, Continent)
#3.) Routes that Depend on User inputs to filter data and render to Visualization

# 1.) Flask Set up and HTML Routes

import os

import pandas as pd
import numpy as np

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


#################################################
# Database Setup
#################################################

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/NBAfantasyML.sqlite"
# db = SQLAlchemy(app)
engine = create_engine("sqlite:///db/NBAfantasyML.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



# Save references to each table
Yearly_Player_Stats2 = Base.classes.Yearly_Player_Stats
# Player_Non_Stat = Base.classes.PLAYER_NON_STAT
# NBA_Teams = Base.classes.NBA_Teams
# Game_Date_Schedule = Base.classes.NBA_SCHEDULE_GAME_DATE


@app.route("/")
def index():

#         return (
#         f"Available Routes:<br/>"
#         f"/api/v1.0/names<br/>"
#         f"/api/v1.0/passengers"
#     )

   results_players = session.query(Yearly_Player_Stats2).all()

   # Create a dictionary from the row data and append to a list of all_players
   all_players = []
   for players in results_players:
       player_dict = {}
       player_dict["personId"] = players.personId
       player_dict["seasonYear"] = players.seasonYear
       all_players.append(player_dict)

   return jsonify(all_players)

if __name__ == "__main__":
   app.run(debug=True)