from flask import Blueprint

grids_bp = Blueprint('grids', __name__)

from .views import *
from .api import *

columns = [
    'x',
    'y',
    'owner',
    'type',
    'color',
]

GRID_TYPES = [
    'oasis',
    'wilderness',
    'space',
    'village',
    'capital',
]