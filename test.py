import pandas as pd
from sqlalchemy import create_engine
import numpy as np

df = pd.read_csv('ipl.csv')
# print(df)

HOST = 'localhost'
PORT = 3306
USERNAME = 'root'
PASS = 'root'
DATABASE = 'ipl_dataset'

try:
    engine = create_engine(
            url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                USERNAME, PASS, HOST, PORT, DATABASE
            )
        )
except Exception as e:
    print(e)

# venues.to_sql('venue', con=engine, if_exists='append', index=False)
# players.to_sql('player', con=engine, if_exists='append', index=False)
# teams.to_sql('teams', con=engine, if_exists='append', index=False)
# umpires.to_sql('umpire', con=engine, if_exists='append', index=False)

venue = pd.read_sql('venue', con=engine)
player = pd.read_sql('player', con=engine)
teams = pd.read_sql('teams', con=engine)
umpire = pd.read_sql('umpire', con=engine)

df['venue'] = df['venue'].map(venue.set_index('stadium')['id'])
df['player_of_match'] = df['player_of_match'].map(player.set_index('name')['id'])
df['team1'] = df['team1'].map(teams.set_index('name')['id'])
df['team2'] = df['team2'].map(teams.set_index('name')['id'])
df['toss_winner'] = df['toss_winner'].map(teams.set_index('name')['id'])
df['winner'] = df['winner'].map(teams.set_index('name')['id'])
df['umpire1'] = df['umpire1'].map(umpire.set_index('name')['id'])
df['umpire2'] = df['umpire2'].map(umpire.set_index('name')['id'])

df = df.drop('city', 1)
df = df.drop('neutral_venue', 1)

df = df.rename(columns={'date':'match_date', 'team1':'team_1',	'team2':'team_2', 'player_of_match':'man_of_the_match', 'winner':'match_winner', 'result':'win_type', 'result_margin':'win_margin', 'umpire1':'umpire_1','umpire2':'umpire_2'
})

# print(df.head(20))
df.to_sql('match', con=engine, if_exists='append', index=False)