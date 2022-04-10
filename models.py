"""Application Models"""
from werkzeug.security import generate_password_hash, check_password_hash
from db import Match, Player, Team, Umpire, Users, Venue, session
from utils import serialize_object




class Players:
    def __init__(self):
        return
    
    def create(self, name):
        try:
            player = self.get_by_name(name)
            if player:
                return

            new_player = Player(
                name = name
            )
            session.add(new_player)
            session.commit()

            return serialize_object(new_player)
        except:
            session.rollback()
            return

    def get_all(self):
        try:
            players = session.query(Player).all()
            return [serialize_object(label) for label in players]
        except:
            session.rollback()
            return

    def get_by_id(self, player_id):
        try:
            player = session.query(Player).filter(Player.id == player_id).first()
            if not player:
                return
            return serialize_object(player)
        except:
            session.rollback()
            return

    def get_by_name(self, player_name):
        try:
            player = session.query(Player).filter(Player.name == player_name).first()
            if not player:
                return
            return serialize_object(player)
        except:
            session.rollback()
            return

    def update(self, player_id, name=""):
        try:
            """Update a player"""
            player = session.query(Player).filter(Player.id == player_id).first()
            player.name = name
            session.commit()
            return serialize_object(player)
        except:
            session.rollback()
            return

    def delete(self, player_id):
        try:
            """Delete a player"""
            session.query(Player).filter(Player.id==player_id).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return

class Umpires:
    def __init__(self):
        return
    
    def create(self, umpire_name):
        try:
            umpire = self.get_by_name(umpire_name)
            if umpire:
                return

            new_umpire = Umpire(
                name = umpire_name
            )
            session.add(new_umpire)
            session.commit()

            return serialize_object(new_umpire)
        except:
            session.rollback()
            return

    def get_all(self):
        try:
            umpires = session.query(Umpire).all()
            return [serialize_object(label) for label in umpires]
        except:
            session.rollback()
            return

    def get_by_id(self, umpire_id):
        try:
            umpire = session.query(Umpire).filter(Umpire.id == umpire_id).first()
            if not umpire:
                return
            return serialize_object(umpire)
        except:
            session.rollback()
            return

    def get_by_name(self, umpire_name):
        try:
            umpire = session.query(Umpire).filter(Umpire.name == umpire_name).first()
            if not umpire:
                return
            return serialize_object(umpire)
        except:
            session.rollback()
            return

    def update(self, umpire_id, umpire_name=""):
        try:
            """Update a umpire"""
            umpire = session.query(Umpire).filter(Umpire.id == umpire_id).first()
            umpire.name = umpire_name
            session.commit()
            return serialize_object(umpire)
        except:
            session.rollback()
            return

    def delete(self, umpire_id):
        try:
            """Delete a umpire"""
            session.query(Umpire).filter(Umpire.id==umpire_id).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return

class Teams:
    def __init__(self):
        return
    
    def create(self, team_name):
        try:
            team = self.get_by_name(team_name)
            if team:
                return

            new_team = Team(
                name = team_name
            )
            session.add(new_team)
            session.commit()

            return serialize_object(new_team)
        except:
            session.rollback()
            return

    def get_all(self):
        try:
            teams = session.query(Team).all()
            return [serialize_object(label) for label in teams]
        except:
            session.rollback()
            return

    def get_by_id(self, team_id):
        try:
            team = session.query(Team).filter(Team.id == team_id).first()
            if not team:
                return
            return serialize_object(team)
        except:
            session.rollback()
            return

    def get_by_name(self, team_name):
        try:
            team = session.query(Team).filter(Team.name == team_name).first()
            if not team:
                return
            return serialize_object(team)
        except:
            session.rollback()
            return

    def update(self, team_id, team_name=""):
        try:
            """Update a team"""
            team = session.query(Team).filter(Team.id == team_id).first()
            team.name = team_name
            session.commit()
            return serialize_object(team)
        except:
            session.rollback()
            return

    def delete(self, team_id):
        try:
            """Delete a team"""
            session.query(Team).filter(Team.id==team_id).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return

class Venues:
    def __init__(self):
        return
    
    def create(self, stadium, city):
        try:
            venue = self.get_by_name(stadium)
            if venue:
                return

            new_venue = Venue(
                stadium = stadium,
                city = city
            )
            session.add(new_venue)
            session.commit()

            return serialize_object(new_venue)
        except:
            session.rollback()
            return

    def get_all(self):
        try:
            venues = session.query(Venue).all()
            return [serialize_object(label) for label in venues]
        except:
            session.rollback()
            return
    
    def get_all_stadiums_by_city(self, city):
        try:
            venues = session.query(Venue).filter(Venue.city == city).all()
            return [serialize_object(label) for label in venues]
        except:
            session.rollback()
            return

    def get_by_id(self, venue_id):
        try:
            venue = session.query(Venue).filter(Venue.id == venue_id).first()
            if not venue:
                return
            return serialize_object(venue)
        except:
            session.rollback()
            return

    def get_by_stadium(self, stadium):
        try:
            venue = session.query(Venue).filter(Venue.stadium == stadium).first()
            if not venue:
                return
            return serialize_object(venue)
        except:
            session.rollback()
            return

    def get_city_by_stadium(self, stadium):
        try:
            venue = session.query(Venue).filter(Venue.stadium == stadium).first()
            return str(venue.city)
        except:
            session.rollback()
            return

    def update(self, venue_id, **data):
        try:
            """Update a venue"""
            session.query(Venue).filter(Venue.id == venue_id).update(data)
            session.commit()
            venue = session.query(Venue).filter(Venue.id == venue_id).first()
            return serialize_object(venue)
        except:
            session.rollback()
            return

    def delete(self, venue_id):
        try:
            """Delete a venue"""
            session.query(Venue).filter(Venue.id==venue_id).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return

class Matches:

    def __init__(self):
        return
    
    def get_by_id(self, match_id):
        try:
            match = session.query(Match).filter(Match.id == match_id).first()
            if match:
                return serialize_object(match)
            else:
                return {}
        except:
            session.rollback()
            return

    def get_all(self):
        try:
            matches = session.query(Match).all()
            if matches:
                return [serialize_object(label) for label in matches]
            else:
                return []
        except:
            session.rollback()
            return

    def create(self, **data):
        try:
            data['team_1'] = Teams().get_by_name(data["team_1"])['id'] if data['team_1'] else None
            data['team_2'] = Teams().get_by_name(data["team_2"])['id'] if data['team_2'] else None
            data['toss_winner'] = Teams().get_by_name(data["toss_winner"])['id'] if data['toss_winner'] else None
            data['match_winner'] = Teams().get_by_name(data["match_winner"])['id'] if data['match_winner'] else None
            data['man_of_the_match'] = Players().get_by_name(data["man_of_the_match"])['id'] if data['man_of_the_match'] else None
            data['umpire_1'] = Umpires().get_by_name(data["umpire_1"])['id'] if data['umpire_1'] else None
            data['umpire_2'] = Umpires().get_by_name(data["umpire_2"])['id'] if data['umpire_2'] else None
            data['venue'] = Venues().get_by_stadium(data["venue"])['id'] if data['venue'] else None

            new_match = Match(**data)
            session.add(new_match)
            session.commit()
            return data
        except:
            session.rollback()
            return

    def get_by_filter(self, **data):
        try:
            query = session.query(Match)

            for attr,value in data.items():
                if value:
                    query = query.filter( getattr(Match,attr)==value )

            matches = query.all()
            if matches:
                matches = [serialize_object(label) for label in matches]
            
                for match in matches:

                    match['team_1'] = Teams().get_by_id(match["team_1"])['name'] if match["team_1"] else None
                    match['team_2'] = Teams().get_by_id(match["team_2"])['name'] if match["team_2"] else None
                    match['toss_winner'] = Teams().get_by_id(match["toss_winner"])['name'] if match["toss_winner"] else None
                    match['match_winner'] = Teams().get_by_id(match["match_winner"])['name'] if match["match_winner"] else None
                    match['man_of_the_match'] = Players().get_by_id(match["man_of_the_match"])['name'] if match["man_of_the_match"] else None
                    match['umpire_1'] = Umpires().get_by_id(match["umpire_1"])['name'] if match["umpire_1"] else None
                    match['umpire_2'] = Umpires().get_by_id(match["umpire_2"])['name'] if match["umpire_2"] else None
                    match['venue'] = Venues().get_by_id(match["venue"])['stadium'] if match["venue"] else None

                return matches
            return []
        except:
            session.rollback()
            return

    def update(self, match_id, **data):
        try:
            session.query(Match).filter(Match.id == match_id).update(data)
            session.commit()
            match = session.query(Match).filter(Match.id == match_id).first()
            return serialize_object(match)
        except:
            session.rollback()
            return

    def delete(self, match_id):
        try:
            session.query(Match).filter(Match.id == match_id).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return

class User:
    """User Model"""
    def __init__(self):
        return

    def create(self, name="", email="", password=""):
        try:
            """Create a new user"""
            user = self.get_by_email(email)
            if user:
                return
            new_user = Users(
                name= name,
                email= email,
                password= self.encrypt_password(password),
                active= True
            )
            session.add(new_user)
            session.commit()
            user = serialize_object(new_user)
            user.pop('password')
            return user
        except:
            session.rollback()
            return

    def get_all(self):
        try:
            """Get all users"""
            users = session.query(Users).filter(Users.active=='1').all()
            if users:
                return [serialize_object(label) for label in users]
            return []
        except:
            session.rollback()
            return

    def get_by_id(self, user_id):
        try:
            """Get a user by id"""
            user = session.query(Users).filter(Users.id==user_id).first()
            if not user:
                return
            user = serialize_object(user)
            user.pop('password')
            return user
        except:
            session.rollback()
            return

    def get_by_email(self, email):
        try:
            """Get a user by email"""
            user = session.query(Users).filter(Users.email==email).first()
            if not user:
                return
            user = serialize_object(user)
            return user
        except:
            session.rollback()
            return

    def update(self, user_id, name=""):
        try:
            """Update a user"""
            data = {}
            if name:
                data["name"] = name
            user = session.query(Users).filter(Users.id==user_id).first()
            user.name = name
            session.commit()
            user = serialize_object(user)
            user.pop('password')
            return user
        except:
            session.rollback()
            return

    def delete(self, user_id):
        try:
            """Delete a user"""
            session.query(Users).filter(Users.id == user_id).delete()
            session.commit()
            return True
        except:
            session.rollback()
            return

    def disable_account(self, user_id):
        try:
            """Disable a user account"""
            user = session.query(Users).filter(Users.id==user_id).first()
            user.active = False
            session.commit()
            user = serialize_object(user)
            user.pop('password')
            return user
        except:
            session.rollback()
            return

    def encrypt_password(self, password):
        try:
            """Encrypt password"""
            return generate_password_hash(password)
        except:
            session.rollback()
            return

    def login(self, email, password):
        try:
            """Login a user"""
            user = self.get_by_email(email)
            if not user or not check_password_hash(user['password'], password):
                return

            user.pop("password")
            return user
        except:
            session.rollback()
            return

