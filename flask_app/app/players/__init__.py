from flask import Blueprint

players_bp = Blueprint('players', __name__)

from .views import *
from .api import *