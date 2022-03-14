from flask import Blueprint, Flask
from pymongo import MongoClient

api_bp = Blueprint('api', __name__)


def create_app():
    
    app = Flask(__name__)
    
    from .players import players_bp
    app.register_blueprint(api_bp, url_prefix='/api/travian')
    app.register_blueprint(players_bp, url_prefix='/travian/players')
    
    return app


class DB(object):

    @staticmethod
    def connect():
        return MongoClient('mongodb://localhost:27017')
