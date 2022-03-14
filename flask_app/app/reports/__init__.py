from flask import Blueprint

reports_bp = Blueprint('reports', __name__)

from .views import *
from .api import *

columns = [
    'x',
    'y',
    'link',
    'image',
    'create_date',
]