from . import players_bp
from flask import render_template


@players_bp.route('/<player_id>', methods=['GET'])
def index(player_id):
    return render_template('player.html', player_id=player_id)
