import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

load_dotenv()

HOST = os.environ.get('DB_HOST')
PORT = os.environ.get('DB_PORT')
USERNAME = os.environ.get('DB_USERNAME')
PASS = os.environ.get('DB_PASS')
DATABASE = os.environ.get('DATABASE')

Base = automap_base()
engine = create_engine(url=os.environ.get('DATABASE_URL').format(USERNAME, PASS, HOST, PORT, DATABASE))
Base.prepare(engine,reflect=True)
session = Session(engine)

Match = Base.classes.match
Umpire = Base.classes.umpire
Team = Base.classes.teams
Player = Base.classes.player
Venue = Base.classes.venue
Users = Base.classes.user