
def get_centre(bbox):
        x1, y1, x2, y2 = bbox
        cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2

        return cx1, cy1

class Heatmap:
     def __init__(self, team_cluster, file_name = "C:/Users/HP/OneDrive/Desktop/football_analysys_web_app/backend/app/prediction/tracked_data/tracked_data.json"):
        self.team_cluster = team_cluster
        self.file_name = file_name

     def create_heatmap(self): 
        import json
        import seaborn as sns
        import matplotlib.pyplot as plt
        import pandas as pd
        import numpy as np
        from mplsoccer import Pitch
        import io

        with open(self.file_name, "r") as f:
            tracked_data = json.load(f)

        team = [player for player in tracked_data['player'] if player['team'] == self.team_cluster]
        pitch = Pitch(pitch_length=105, pitch_width=90,
              pitch_color='green', stripe=False )

        fig, ax = pitch.draw(figsize=(16, 9))

        centers_x = []
        centers_y = []
        for player in team:
            cx, cy = get_centre(player['bbox'])
            centers_x.append(cx)
            centers_y.append(cy)

        centers_y_modified = [1080 - y for y in centers_y]
        centers_y_modified_meters = (np.array(centers_y_modified) / 1080) * 90
        centers_x_meters = (np.array(centers_x) / 1920) * 105

        sns.kdeplot(
            x=centers_x_meters,
            y=centers_y_modified_meters,
            cmap="inferno",
            fill=True,
            thresh=0.05,
            alpha=0.5,
            clip=((0, 1920), (0, 1080)),
            bw_adjust=0.6,
        )
        ax.set_aspect('equal')
        plt.tight_layout()
        

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        

        return buf
