from ultralytics import YOLO
from sports.annotators.soccer import draw_pitch
from sports.configs.soccer import SoccerPitchConfiguration
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import io
import os
from dotenv import load_dotenv

load_dotenv()

class Heatmap:
     def __init__(self, team_cluster):
        self.team_cluster = team_cluster
        self.file_name = os.getenv("TRACKED_FILE")
        self.model = YOLO(os.getenv("KEYPOINTS_MODEL"))
        self.pitch_config = SoccerPitchConfiguration()
        self.projected_points_file = os.getenv("PROJECTED_POINTS_PATH") 

     def _get_bottom_center(self,bbox):
        x1, y1, x2, y2 = bbox
        x_center = (x1 + x2) / 2
        y_bottom = y2
        return (x_center, y_bottom)

      
     def _read_data(self):
            with open(self.projected_points_file, "r") as f:
                projected_data = json.load(f) 
            return projected_data


     
     def create_heatmap(self): 
      scale = 0.1
      padding = 50
      all_projected_points = []

      projected_data = self._read_data()
      key = f'team_{self.team_cluster}'
      cluster_points = projected_data.get(key, [])
      if cluster_points is not None:
          all_projected_points.extend(cluster_points)
      else:
          raise ValueError(f"No projected points found for team cluster: {self.team_cluster}")

      if not all_projected_points:
         raise ValueError("No valid player points found for heatmap.")
      
      print('Procesare heatmap')
      pitch_players_xy = np.array(all_projected_points) * scale + padding

      valid_mask = (
            (pitch_players_xy[:, 0] >= padding) & (pitch_players_xy[:, 0] <= padding + self.pitch_config.length * scale) &
            (pitch_players_xy[:, 1] >= padding) & (pitch_players_xy[:, 1] <= padding + self.pitch_config.width * scale)
        )
      pitch_players_xy = pitch_players_xy[valid_mask]

      x = pitch_players_xy[:, 0]
      y = pitch_players_xy[:, 1]

      pitch = draw_pitch(self.pitch_config, scale=scale, padding=padding)

      fig, ax = plt.subplots(figsize=(12, 8))
      ax.imshow(pitch, extent=[0, pitch.shape[1], 0, pitch.shape[0]])

      print('Drawing heatmap')
      print(f"Number of points: {len(x)}")
      if len(x) >= 3:
         
            sns.kdeplot(
                x=x,
                y=y,
                cmap="hot",
                fill=True,
                thresh=0.05,
                alpha=0.5,
                clip=(
                    (padding, padding + self.pitch_config.length * scale),
                    (padding, padding + self.pitch_config.width * scale)
                ),
                bw_adjust=0.7,
                ax=ax
            )

      ax.set_xlim(0, pitch.shape[1])
      ax.set_ylim(0, pitch.shape[0])
      ax.invert_yaxis()
      ax.set_aspect('equal')
      plt.axis('off')
      plt.tight_layout()

      buf = io.BytesIO()
      plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
      buf.seek(0)
      plt.close()

      return buf
