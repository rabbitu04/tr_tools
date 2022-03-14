import json
from app import create_app, DB
from flask import render_template
from app.players.api import player_list

app = create_app()


@app.route('/hello-world', methods=['GET'])
def hello_world():
    return {'hello': 'world'}


@app.route('/test-db', methods=['GET'])
def test_db():
    mongo = DB.connect()
    db = mongo['testDB']
    obj = db.test.find_one({}, {'_id': 0})
    return dict(obj)

@app.route('/travian/index', methods=['GET'])
def tr_index():
    players = player_list()['players']
    players_dict = dict()
    for player in players:
        if player['alliance'] not in players_dict:
            players_dict[player['alliance']] = list()
        players_dict[player['alliance']].append(player)
    
    return render_template('index.html', alliances=players_dict)
