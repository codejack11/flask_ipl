from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


HOST = 'localhost'
PORT = 3306
USERNAME = 'root'
PASS = 'root'
DATABASE = 'ipl_dataset'

Base = automap_base()
engine = create_engine(url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                USERNAME, PASS, HOST, PORT, DATABASE
            ), isolation_level="READ UNCOMMITTED")
Base.prepare(engine,reflect=True)
session = Session(engine)

Match = Base.classes.match
Umpire = Base.classes.umpire
Teams = Base.classes.teams
Player = Base.classes.player
Venue = Base.classes.venue
User = Base.classes.user