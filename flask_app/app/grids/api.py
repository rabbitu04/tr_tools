from .. import api_bp, DB
from grids import GRID_TYPES


@api_bp.route('/plotly_grids', methods=['GET'])
def plotly_grid_list():
    mongo = DB.connect()
    db = monog['travian']

    output = dict()
    for gt in GRID_TYPES:
        output[gt] = list()

    grids = db.grids.find()
    grid_data = {
        'x': list(),
        'y': list(),
        # 'color': list(),
        'border_color': list(),
    }

    for grid in grids:
        grid_data['x'].append(grid['x'])
        grid_data['y'].append(grid['y'])
        # grid_data['color'].append()
        grid_data['border_color'].append(grid['color'])
        
    return grids
