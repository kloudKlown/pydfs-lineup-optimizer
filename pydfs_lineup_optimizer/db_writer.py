import mysql.connector
from mysql import *
import re
import os
from sqlalchemy import create_engine, exc
import pandas as pd
from tqdm import tqdm
from pydfs_lineup_optimizer.lineup import Lineup
from pydfs_lineup_optimizer.player import Player
import json

dbEngine = create_engine("mysql+pymysql://{user}:{pw}@localhost:{port}/{db}".format(user="root",pw="FF123",port = '3361', db="DailyFantasyQ"))
query = "INSERT INTO DK_Lineups (LineupID, GameID, Lineup, Projection, Salary, Actual)\
     VALUES(%s, %s, %s, %s, %s, %s);"

def PrintLineups(LP, gameID):
    # df = pd.read_csv(fileName)
    # GameID = int(df["GameID"].iloc[0])
    dbEngine.execute("DELETE FROM DK_Lineups WHERE GameID = " + str(gameID)+";")
    lineupID = 1
    for each in LP:                    
        lineups = []
        
        for p in each.players:            
            lineups.append(get_json(p))
        vals = [lineupID, gameID, json.dumps(lineups), each.fantasy_points_projection, each.salary_costs, each.actual]
        dbEngine.execute(query, tuple(vals))
        lineupID += 1
        
def get_json(player):
    player_json = {}
    player_json["ID"] = int(player.id)
    player_json["Name"] = '{} {}'.format(player.first_name, player.last_name)
    player_json["NAME + ID"] = player_json["Name"] + "(" + str(player.id) + ")"
    player_json["Team"] = player.team
    player_json["Positions"] = player.positions[0]
    player_json["Salary"] = player.salary
    player_json["Fppg"] = player.fppg
    player_json["Actual"] = player.actual
    return player_json