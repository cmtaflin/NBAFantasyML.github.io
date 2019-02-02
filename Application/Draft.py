# This code runs the machine learning functions for the fantasy draft
# Structure of file
#1.) calculate the zscore for 9 categories
#2.) primary function - log_regression


# dependencies
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sqlalchemy import create_engine, inspect, func, distinct
import sqlite3
from sqlite3 import Error

#setup the database connection
#def enginetest():
    #engine = create_engine("sqlite:///db/NBA_Data.sqlite")
    
def conntest():
    engine = create_engine("sqlite:///db/NBA_Data.sqlite")
    conn = engine.connect()
    return conn

#engine.table_names()

# this function calculates the z-scores for 9-Categories and ranks players based on average z-score
# the input df has a column TOP if top players have been predicted by the logistic model
# otherwise, the top players will be ranked by VORP
def zscore(df, sample_size=130, min_games=10):

    
    if "TOP" in df.columns:
        sample_size = df["TOP"].sum()
        top_players = df[df["TOP"]==1]
    else:
        top_players = df.sort_values("VORP", ascending = False).head(sample_size)
        top_players["TOP"] = 1
        df = pd.merge(top_players[["Player", "TOP"]], df, on="Player", how="outer").fillna(0)

    # calculate adjusted percentages
    top_players['adj_FG'] = (10*(top_players['FG'].sum() / sample_size) + top_players["FG"]) / (10*(top_players['FGA'].sum() / sample_size) + top_players["FGA"])
    top_players['adj_FT'] = (10*(top_players['FT'].sum() / sample_size) + top_players["FT"]) / (10*(top_players['FTA'].sum() / sample_size) + top_players["FTA"])
    df['adj_FG'] = (10*(top_players['FG'].sum() / sample_size) + df["FG"]) / (10*(top_players['FGA'].sum() / sample_size) + df["FGA"])
    df['adj_FT'] = (10*(top_players['FT'].sum() / sample_size) + df["FT"]) / (10*(top_players['FTA'].sum() / sample_size) + df["FTA"])

    # calculate z-scores and average z-score
    df["zFG"] = (df["adj_FG"] - top_players["adj_FG"].mean()) / top_players["adj_FG"].std()
    df["zFT"] = (df["adj_FT"] - top_players["adj_FT"].mean()) / top_players["adj_FT"].std()
    df["z3P"] = (df["3P"] - top_players["3P"].mean()) / top_players["3P"].std()
    df["zPTS"] = (df["PTS"] - top_players["PTS"].mean()) / top_players["PTS"].std()
    df["zREB"] = (df["TRB"] - top_players["TRB"].mean()) / top_players["TRB"].std()
    df["zAST"] = (df["AST"] - top_players["AST"].mean()) / top_players["AST"].std()
    df["zSTL"] = (df["STL"] - top_players["STL"].mean()) / top_players["STL"].std()
    df["zBLK"] = (df["BLK"] - top_players["BLK"].mean()) / top_players["BLK"].std()
    df["zTOV"] = (top_players["TOV"].mean() - df["TOV"]) / top_players["TOV"].std()
    df["zAVG"] = (df["zFG"] + df["zFT"] + df["z3P"] + df["zPTS"] + df["zREB"] + df["zAST"] + df["zSTL"] + df["zBLK"] + df["zTOV"]) / 9

    # rank by avg z-score
    df = df.sort_values("zAVG", ascending = False).reset_index(drop=True)
    df.index += 1
    
    # exclude players with less than a set amount of games (default 10)
    df = df[df.G >= min_games]
    
    return df;


# season (int): the first season is used to train the model to predict top players for the next year
# roster_size (int): number of players per team in the league
# num_teams (int): number of teams in the fantasy league
# min_games (int): minimum number of games to include player on chart
def log_regression(season, roster_size = 13, num_teams = 10, min_games = 10):
    
    conn = conntest()    
    
    df = pd.read_sql(f'select * from season_{season}_{season+1}', conn)
    
    #file_to_load = f"Resources/{season}_{season+1}.csv"
    #df = pd.read_csv(file_to_load)
    
    sample_size = roster_size*num_teams

    df = zscore(df, sample_size)
    
    # Assign X (data) and y (target)
    X = df.drop(["Player", "TOP", "Rookie", "Pos", "G", "VORP"], axis=1)
    y = df["TOP"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)
    
    classifier = LogisticRegression()
    
    classifier.fit(X_train, y_train)
    
    print(f"Training Data Score: {classifier.score(X_train, y_train)}")
    print(f"Testing Data Score: {classifier.score(X_test, y_test)}")
    
    predictions = classifier.predict(X_test)
    print(f"First 10 Predictions:   {predictions[:10]}")
    print(f"First 10 Actual labels: {y_test[:10].tolist()}")
    
    #next_season = f"{season+1}_{season+2}"

    #file_to_load = f"Resources/{next_season}.csv"
    #next_df = pd.read_csv(file_to_load)
    
    next_df = pd.read_sql(f'select * from season_{season+1}_{season+2}', conn)
    
    next_df = zscore(next_df, sample_size)
    X = next_df.drop(["TOP","Player", "Rookie", "Pos", "G", "VORP"], axis=1).fillna(0)
    predictions = classifier.predict(X)
    
    next_df["TOP"] = predictions
    print(f"z-score calculated with {next_df['TOP'].sum()} top players")
    next_df = zscore(next_df, sample_size)
    next_df.index.name = "Rank"
    #next_df.to_csv(f"Resources/log_rank_{season+2}_{season+3}.csv", index=True)
    
    return next_df