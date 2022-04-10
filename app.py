import jwt, os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from validate import validate_match, validate_email_and_password, validate_user
from flask_cors import CORS, cross_origin

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
# print(SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY

from models import Matches, Players, Teams, Umpires, User, Venues
from auth_middleware import token_required

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/users/", methods=["POST"])
def add_user():
    try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        is_validated = validate_user(**user)
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().create(**user)
        if not user:
            return {
                "message": "User already exists",
                "error": "Conflict",
                "data": None
            }, 409
        return {
            "message": "Successfully created new user",
            "data": user
        }, 201
    except Exception as e:
        return {
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }, 500

@app.route("/api/users/login", methods=["POST"])
def login():
    try:
        data = request.json
        if not data:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        # validate input
        is_validated = validate_email_and_password(data.get('email'), data.get('password'))
        if is_validated is not True:
            return dict(message='Invalid data', data=None, error=is_validated), 400
        user = User().login(
            data["email"],
            data["password"]
        )
        if user:
            try:
                # token should expire after 24 hrs
                user["token"] = jwt.encode(
                    {"user_id": user["id"]},
                    app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user
                }
            except Exception as e:
                return {
                    "error": "Something went wrong",
                    "message": str(e)
                }, 500
        return {
            "message": "Error fetching auth token!, invalid email or password",
            "data": None,
            "error": "Unauthorized"
        }, 404
    except Exception as e:
        return {
                "message": "Something went wrong!",
                "error": str(e),
                "data": None
        }, 500


@app.route("/api/users/", methods=["GET"])
@token_required
def get_current_user(current_user):
    return jsonify({
        "message": "successfully retrieved user profile",
        "data": current_user
    })

@app.route("/api/users/", methods=["PUT"])
@token_required
def update_user(current_user):
    try:
        user = request.json
        if user.get("name"):
            user = User().update(current_user["id"], user["name"])
            return jsonify({
                "message": "successfully updated account",
                "data": user
            }), 201
        return {
            "message": "Invalid data, you can only update your account name!",
            "data": None,
            "error": "Bad Request"
        }, 400
    except Exception as e:
        return jsonify({
            "message": "failed to update account",
            "error": str(e),
            "data": None
        }), 400

@app.route("/api/users/", methods=["DELETE"])
@token_required
def disable_user(current_user):
    try:
        User().disable_account(current_user["id"])
        return jsonify({
            "message": "successfully disabled acount",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to disable account",
            "error": str(e),
            "data": None
        }), 400

@app.route("/api/matches/", methods=["POST"])
@token_required
def add_match(current_user):
    try:
        match = dict(request.form)
        if not match:
            return {
                "message": "Invalid data, you need to provide proper details",
                "data": None,
                "error": "Bad Request"
            }, 400
        # if not request.files["cover_image"]:
        #     return {
        #         "message": "cover image is required",
        #         "data": None
        #     }, 400

        # match["image_url"] = request.host_url+"static/books/"+save_pic(request.files["cover_image"])
        is_validated = validate_match(**match)
        if is_validated is not True:
            return {
                "message": "Invalid data",
                "data": None,
                "error": is_validated
            }, 400
        match = Matches().create(**match, user_id=current_user["id"])
        if not match:
            return {
                "message": "The match has been created by user",
                "data": None,
                "error": "Conflict"
            }, 400
        return jsonify({
            "message": "successfully created a new match",
            "data": match
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to create a new match",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/matches/", methods=["GET"])
@token_required
def get_matches(current_user):
    try:
        matches = Matches().get_all()
        return jsonify({
            "message": "successfully retrieved all matches",
            "data": matches
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all matches",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/search/match", methods=["POST"])
@token_required
def get_matches_by_filter(current_user):
    try:
        search_filter = dict(request.form)
        if not search_filter:
            return {
                "message": "Invalid data, you need to provide proper details",
                "data": None,
                "error": "Bad Request"
            }, 400
        matches = Matches().get_by_filter(search_filter)
        return jsonify({
            "message": "successfully retrieved all matches",
            "data": matches
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all matches",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/matches/<match_id>", methods=["GET"])
@token_required
def get_match(match_id):
    try:
        match = Matches().get_by_id(match_id)
        if not match:
            return {
                "message": "Match not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a match",
            "data": match
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/matches/<match_id>", methods=["PUT"])
@token_required
def update_match(current_user, match_id):
    try:
        match = Matches().get_by_id(match_id)
        if not match:
            return {
                "message": "Match not found",
                "data": None,
                "error": "Not found"
            }, 404
        match = request.form
        # if match.get('cover_image'):
        #     match["image_url"] = request.host_url+"static/matches/"+save_pic(request.files["cover_image"])
        match = Matches().update(match_id, **match)
        return jsonify({
            "message": "successfully updated a match",
            "data": match
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to update a match",
            "error": str(e),
            "data": None
        }), 400

@app.route("/api/matches/<match_id>", methods=["DELETE"])
@token_required
def delete_match(current_user, match_id):
    try:
        match = Matches().get_by_id(match_id)
        if not match:
            return {
                "message": "Match not found",
                "data": None,
                "error": "Not found"
            }, 404
        Matches().delete(match_id)
        return jsonify({
            "message": "successfully deleted a match",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to delete a match",
            "error": str(e),
            "data": None
        }), 400

@app.route("/api/players/", methods=["GET"])
@token_required
def get_players(current_user):
    try:
        players = Players().get_all()
        return jsonify({
            "message": "successfully retrieved all players",
            "data": players
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all players",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/players/<player_id>", methods=["GET"])
@token_required
def get_player(player_id):
    try:
        player = Players().get_by_id(player_id)
        if not player:
            return {
                "message": "Player not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a player",
            "data": player
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/teams/", methods=["GET"])
@token_required
def get_teams(current_user):
    try:
        teams = Teams().get_all()
        return jsonify({
            "message": "successfully retrieved all teams",
            "data": teams
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all teams",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/teams/<team_id>", methods=["GET"])
@token_required
def get_team(team_id):
    try:
        team = Teams().get_by_id(team_id)
        if not team:
            return {
                "message": "Team not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a team",
            "data": team
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/umpires/", methods=["GET"])
@token_required
def get_umpires(current_user):
    try:
        umpires = Umpires().get_all()
        return jsonify({
            "message": "successfully retrieved all umpires",
            "data": umpires
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all umpires",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/umpires/<umpire_id>", methods=["GET"])
@token_required
def get_umpire(umpire_id):
    try:
        umpire = Umpires().get_by_id(umpire_id)
        if not umpire:
            return {
                "message": "Umpire not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a umpire",
            "data": umpire
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/venues/", methods=["GET"])
@token_required
def get_venues(current_user):
    try:
        venues = Venues().get_all()
        return jsonify({
            "message": "successfully retrieved all venues",
            "data": venues
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all venues",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/venues/<venue_id>", methods=["GET"])
@token_required
def get_venue(venue_id):
    try:
        venue = Venues().get_by_id(venue_id)
        if not venue:
            return {
                "message": "Venue not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a venue",
            "data": venue
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.errorhandler(403)
def forbidden(e):
    return jsonify({
        "message": "Forbidden",
        "error": str(e),
        "data": None
    }), 403

@app.errorhandler(404)
def forbidden(e):
    return jsonify({
        "message": "Endpoint Not Found",
        "error": str(e),
        "data": None
    }), 404


if __name__ == "__main__":
    app.run(debug=True)
