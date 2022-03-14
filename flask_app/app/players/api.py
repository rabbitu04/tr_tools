from .. import api_bp, DB
from collections import defaultdict
from datetime import datetime, timedelta
from flask import request
from pymongo import MongoClient


@api_bp.route('/players', methods=['GET', 'POST'])
def player_list():

    mongo = DB.connect()
    db = mongo['travian']
    try:
        player_id = int(request.args.get('player_id') or 0)
    except ValueError:
        return {
            'status': False,
            'msg': 'player_id should be integer'
        }

    if request.method == 'POST' and player_id:
        output = {
            'status': False,
            'msg': 'Play already exist'
        }
        if db.players.find_one({'player_id': player_id}):
            return output
        db.players.insert_one({'player_id': player_id})
        output['status'] = True
        output['msg'] = 'Success'
        return output
    
    if player_id:
        player = db.player_basic_data.find({'player_id': player_id}).sort([('_id', -1)]).limit(1)[0]
        return {
            'name': player['name'],
            'alliance': player['alliance']
        }

    last_record = db.player_basic_data.find().sort([('_id', -1)]).limit(1)
    records = db.player_basic_data.find({'date': last_record[0]['date'], 'hour': last_record[0]['hour']}).sort('name')
    players = [{
        'id': player['player_id'],
        'name': player['name'],
        'alliance': player['alliance'],
    } for player in records]

    return {'players': players}


@api_bp.route('/player/delete/<player_id>', methods=['POST'])
def delete_player(player_id):
    
    try:
        player_id = int(player_id)
    except ValueError:
        return {
            'status': False,
            'msg': 'player id should be integer'
        }
    mongo = DB.connect()
    db = mongo['travian']
    output = {
        'status': False,
        'msg': 'Player does not exist'
    }
    player = db.players.find_one({'player_id': player_id})
    if player:
        db.players.delete_one({'player_id': player_id})
        output['status'] = True
        output['msg'] = 'Success'
    return output


@api_bp.route('/inhabitant', methods=['GET'])
@api_bp.route('/inhabitant/<player_id>', methods=['GET'])
def inhabitants(player_id=None):
    
    if not player_id:
        try:
            player_id = int(request.args.get('player_id') or 0)
        except ValueError:
            return {'status': 'fail'}
    
    mongo = DB.connect()
    db = mongo['travian']
    records = db.inhabitants_record.find({'player_id': player_id}, {'_id': 0})
    if records.count() == 0:
        return {'status': 'fail'}
    output = dict()
    output['status'] = 'success'
    output['records'] = dict()

    temp_inhabitant = dict()

    for record in records:
        dt = datetime(
            year=int(record['date'][0:4]),
            month=int(record['date'][5:7]),
            day=int(record['date'][8:10]),
            hour=record['hour']
        ) + timedelta(hours=8)
        coordinate = record['coordinate'].replace('\u202c', '')
        coordinate = coordinate.replace('\u202d', '')
        d = dt.strftime('%Y-%m-%d')
        if d not in output['records']:
            output['records'][d] = defaultdict(lambda : {
                'hour': list(),
                'inhabitant': list(),
                'delta': list(),
            })
        if coordinate not in temp_inhabitant:
            temp_inhabitant[coordinate] = record['inhabitant']
        output['records'][d][coordinate]['hour'].append(dt.hour)
        output['records'][d][coordinate]['inhabitant'].append(record['inhabitant'])
        output['records'][d][coordinate]['delta'].append(record['inhabitant'] - temp_inhabitant[coordinate])
        temp_inhabitant[coordinate] = record['inhabitant']
    return output


@api_bp.route('/points&exp', methods=['GET'])
@api_bp.route('/points&exp/<player_id>', methods=['GET'])
def points_and_exp(player_id=None):

    if not player_id:
        try:
            player_id = int(request.args.get('player_id') or 0)
        except ValueError:
            return {'status': 'fail'}
    output = {
        'status': 'success',
        'records': dict(),
    }
    mongo = DB.connect()
    db = mongo['travian']
    off_points = list(db.off_point.find({'player_id': player_id}))
    def_points = list(db.def_point.find({'player_id': player_id}))
    exps = list(db.exp.find({'player_id': player_id}))
    temp = {
        'off-point': off_points[0]['point'],
        'def-point': def_points[0]['point'],
        'exp': exps[0]['exp']
    }
    for i in range(len(off_points)):
        dt = datetime(
            year=int(off_points[i]['date'][0:4]),
            month=int(off_points[i]['date'][5:7]),
            day=int(off_points[i]['date'][8:10]),
            hour=off_points[i]['hour']
        ) + timedelta(hours=8)
        d = dt.strftime('%Y-%m-%d')
        if d not in output['records']:
            output['records'][d] = {
                'hour': list(),
                'off-point': list(),
                'off-point-delta': list(),
                'def-point': list(),
                'def-point-delta': list(),
                'exp': list(),
                'exp-delta': list(),
            }
        
        output['records'][d]['hour'].append(dt.hour)
        output['records'][d]['off-point'].append(off_points[i]['point'])
        output['records'][d]['off-point-delta'].append(off_points[i]['point'] - temp['off-point'])
        temp['off-point'] = off_points[i]['point']
        output['records'][d]['def-point'].append(def_points[i]['point'])
        output['records'][d]['def-point-delta'].append(def_points[i]['point'] - temp['def-point'])
        temp['def-point'] = def_points[i]['point']
        output['records'][d]['exp'].append(exps[i]['exp'])
        output['records'][d]['exp-delta'].append(exps[i]['exp'] - temp['exp'])
        temp['exp'] = exps[i]['exp']
    return output
