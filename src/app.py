"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Episode, Favorites
from sqlalchemy import select
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/character', methods=['GET'])
def get_character():
    character = db.session.execute(select(Character)).scalars().all()
    transformed = [char.serialize() for char in character]
  
    return jsonify({"success": True, "data": transformed}), 200

@app.route('/episode', methods=['GET'])
def get_episode():
    episode = db.session.execute(select(Episode)).scalars().all()
    transformed = [epi.serialize() for epi in episode]
  
    return jsonify({"success": True, "data": transformed}), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = db.session.execute(select(Favorites)).scalars().all()
    transformed = [fav.serialize() for fav in favorites]
  
    return jsonify({"success": True, "data": transformed}), 200


@app.route('/favorite/character/<int:char_id>', methods=['POST'])
def add_favorite_character(char_id):
    user_id = 1
    new_fav = Favorites(user_id=user_id, character_id=char_id)

    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"success" : True, "msg": "Añadido favorito"}), 201

@app.route('/favorite/episode/<int:epi_id>', methods=['POST'])
def add_favorite_episode(epi_id):
    user_id = 1
    new_fav = Favorites(user_id=user_id, episode_id= epi_id)

    db.session.add(new_fav)
    db.session.commit()

    return jsonify({"success" : True, "msg": "Añadido favorito"}), 201

@app.route("/favorite/character/<int:char_id>", methods=["DELETE"])
def delete_favorite_character(char_id):
    user_id = 1
    fav_delete = db.session.execute(db.select(Favorites).filter_by(user_id=1, character_id=char_id)).scalar_one_or_none()
    if fav_delete:
        db.session.delete(fav_delete)
        db.session.commit()
        return jsonify({"success": True, "msg": f"Favorito personaje {char_id} eliminado"}), 200
    else:
        return jsonify({"success": False, "msg": "Ese favorito personaje no existe"}), 404

@app.route("/favorite/episode/<int:epi_id>", methods=["DELETE"])
def delete_favorite_episode(epi_id):
    user_id = 1
    fav_delete = db.session.execute(db.select(Favorites).filter_by(user_id=1, episode_id=epi_id)).scalar_one_or_none()
    if fav_delete:
        db.session.delete(fav_delete)
        db.session.commit()
        return jsonify({"success": True, "msg": f"Favorito episodio {epi_id} eliminado"}), 200
    else:
        return jsonify({"success": False, "msg": "Ese favorito episodio no existe"}), 404
    
  
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
