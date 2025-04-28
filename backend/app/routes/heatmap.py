import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from prediction.team_heatmap import Heatmap
from flask import Blueprint, request, send_file

heatmap_bp = Blueprint('heatmap_bp', __name__)

@heatmap_bp.route('/createHeatmap', methods=['POST'])
def create_heatmap():
    data = request.json
    team_cluster = data['team_cluster']
    team_name = data['team_name']
    
    
    heatmap = Heatmap(team_cluster)
    heatmap_buf = heatmap.create_heatmap()
    
    heatmap_buf.seek(0)

    return send_file(
        heatmap_buf,
        mimetype='image/png',  
        as_attachment=True,
        download_name=f"{team_name}_heatmap.png" 
    )