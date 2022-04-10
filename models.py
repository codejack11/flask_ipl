"""Application Models"""
from werkzeug.security import generate_password_hash, check_password_hash
from db import Match, Player, Team, Umpire, Users, Venue, session
from utils import serialize_object




class Players:
    def __init__(self):
        return
    
    def create(self, name):
        player = self.get_by_name(name)
        if player:
            return

        new_player = Player(
            name = name
        )
        session.add(new_player)
        session.commit()

        return serialize_object(new_player)

    def get_all(self):
        players = session.query(Player).all()
        return [serialize_object(label) for label in players]

    def get_by_id(self, player_id):
        player = session.query(Player).filter(Player.id == player_id).first()
        if not player:
            return
        return serialize_object(player)

    def get_by_name(self, player_name):
        player = session.query(Player).filter(Player.name == player_name).first()
        if not player:
            return
        return serialize_object(player)

    def update(self, player_id, name=""):
        """Update a player"""
        player = session.query(Player).filter(Player.id == player_id).first()
        player.name = name
        session.commit()
        return serialize_object(player)

    def delete(self, player_id):
        """Delete a player"""
        session.query(Player).filter(Player.id==player_id).delete()
        session.commit()
        return True

class Umpires:
    def __init__(self):
        return
    
    def create(self, umpire_name):
        umpire = self.get_by_name(umpire_name)
        if umpire:
            return

        new_umpire = Umpire(
            name = umpire_name
        )
        session.add(new_umpire)
        session.commit()

        return serialize_object(new_umpire)

    def get_all(self):
        umpires = session.query(Umpire).all()
        return [serialize_object(label) for label in umpires]

    def get_by_id(self, umpire_id):
        umpire = session.query(Umpire).filter(Umpire.id == umpire_id).first()
        if not umpire:
            return
        return serialize_object(umpire)

    def get_by_name(self, umpire_name):
        umpire = session.query(Umpire).filter(Umpire.name == umpire_name).first()
        if not umpire:
            return
        return serialize_object(umpire)

    def update(self, umpire_id, umpire_name=""):
        """Update a umpire"""
        umpire = session.query(Umpire).filter(Umpire.id == umpire_id).first()
        umpire.name = umpire_name
        session.commit()
        return serialize_object(umpire)

    def delete(self, umpire_id):
        """Delete a umpire"""
        session.query(Umpire).filter(Umpire.id==umpire_id).delete()
        session.commit()
        return True

class Teams:
    def __init__(self):
        return
    
    def create(self, team_name):
        team = self.get_by_name(team_name)
        if team:
            return

        new_team = Team(
            name = team_name
        )
        session.add(new_team)
        session.commit()

        return serialize_object(new_team)

    def get_all(self):
        teams = session.query(Team).all()
        return [serialize_object(label) for label in teams]

    def get_by_id(self, team_id):
        team = session.query(Team).filter(Team.id == team_id).first()
        if not team:
            return
        return serialize_object(team)

    def get_by_name(self, team_name):
        team = session.query(Team).filter(Team.name == team_name).first()
        if not team:
            return
        return serialize_object(team)

    def update(self, team_id, team_name=""):
        """Update a team"""
        team = session.query(Team).filter(Team.id == team_id).first()
        team.name = team_name
        session.commit()
        return serialize_object(team)

    def delete(self, team_id):
        """Delete a team"""
        session.query(Team).filter(Team.id==team_id).delete()
        session.commit()
        return True

class Venues:
    def __init__(self):
        return
    
    def create(self, stadium, city):
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

    def get_all(self):
        venues = session.query(Venue).all()
        return [serialize_object(label) for label in venues]
    
    def get_all_stadiums_by_city(self, city):
        venues = session.query(Venue).filter(Venue.city == city).all()
        return [serialize_object(label) for label in venues]

    def get_by_id(self, venue_id):
        venue = session.query(Venue).filter(Venue.id == venue_id).first()
        if not venue:
            return
        return serialize_object(venue)

    def get_by_stadium(self, stadium):
        venue = session.query(Venue).filter(Venue.stadium == stadium).first()
        if not venue:
            return
        return serialize_object(venue)

    def get_city_by_stadium(self, stadium):
        venue = session.query(Venue).filter(Venue.stadium == stadium).first()
        return str(venue.city)

    def update(self, venue_id, **data):
        """Update a venue"""
        session.query(Venue).filter(Venue.id == venue_id).update(data)
        session.commit()
        venue = session.query(Venue).filter(Venue.id == venue_id).first()
        return serialize_object(venue)

    def delete(self, venue_id):
        """Delete a venue"""
        session.query(Venue).filter(Venue.id==venue_id).delete()
        session.commit()
        return True

class Matches:

    def __init__(self):
        return
    
    def get_by_id(self, match_id):
        match = session.query(Match).filter(Match.id == match_id).first()
        return serialize_object(match)

    def get_all(self):
        matches = session.query(Match).all()
        return [serialize_object(label) for label in matches]

    def create(self, **data):
        data['team_1'] = Teams().get_by_name(data["team_1"])['id']
        data['team_2'] = Teams().get_by_name(data["team_2"])['id']
        data['toss_winner'] = Teams().get_by_name(data["toss_winner"])['id']
        data['match_winner'] = Teams().get_by_name(data["match_winner"])['id']
        data['man_of_the_match'] = Players().get_by_name(data["man_of_the_match"])['id']
        data['umpire_1'] = Umpires().get_by_name(data["umpire_1"])['id']
        data['umpire_2'] = Umpires().get_by_name(data["umpire_2"])['id']
        data['venue'] = Venues().get_by_stadium(data["venue"])['id']

        new_match = Match(**data)
        session.add(new_match)
        session.commit()
        return data

    def get_by_filter(self, **data):
        query = session.query(Match)

        for attr,value in data.items():
            query = query.filter( getattr(Match,attr)==value )

        matches = query.all()
        matches = [serialize_object(label) for label in matches]
        
        for match in matches:

            match['team_1'] = Teams().get_by_id(match["team_1"])['name']
            match['team_2'] = Teams().get_by_id(match["team_2"])['name']
            match['toss_winner'] = Teams().get_by_id(match["toss_winner"])['name']
            match['match_winner'] = Teams().get_by_id(match["match_winner"])['name']
            match['man_of_the_match'] = Players().get_by_id(match["man_of_the_match"])['name']
            match['umpire_1'] = Umpires().get_by_id(match["umpire_1"])['name']
            match['umpire_2'] = Umpires().get_by_id(match["umpire_2"])['name']
            match['venue'] = Venues().get_by_id(match["venue"])['stadium']

        return matches

    def update(self, match_id, **data):
        session.query(Match).filter(Match.id == match_id).update(data)
        session.commit()
        match = session.query(Match).filter(Match.id == match_id).first()
        return serialize_object(match)

    def delete(self, match_id):
        session.query(Match).filter(Match.id == match_id).delete()
        session.commit()
        return True

class User:
    """User Model"""
    def __init__(self):
        return

    def create(self, name="", email="", password=""):
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

    def get_all(self):
        """Get all users"""
        users = session.query(Users).filter(Users.active=='1').all()
        return [serialize_object(label) for label in users]

    def get_by_id(self, user_id):
        """Get a user by id"""
        user = session.query(Users).filter(Users.id==user_id).first()
        if not user:
            return
        user = serialize_object(user)
        user.pop('password')
        return user

    def get_by_email(self, email):
        """Get a user by email"""
        user = session.query(Users).filter(Users.email==email).first()
        if not user:
            return
        user = serialize_object(user)
        return user

    def update(self, user_id, name=""):
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

    def delete(self, user_id):
        """Delete a user"""
        session.query(Users).filter(Users.id == user_id).delete()
        session.commit()
        return True

    def disable_account(self, user_id):
        """Disable a user account"""
        user = session.query(Users).filter(Users.id==user_id).first()
        user.active = False
        session.commit()
        user = serialize_object(user)
        user.pop('password')
        return user

    def encrypt_password(self, password):
        """Encrypt password"""
        return generate_password_hash(password)

    def login(self, email, password):
        """Login a user"""
        user = self.get_by_email(email)
        if not user or not check_password_hash(user['password'], password):
            return

        user.pop("password")
        return user

