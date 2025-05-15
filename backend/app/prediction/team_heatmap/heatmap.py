from ultralytics import YOLO
from sports.configs.soccer import SoccerPitchConfiguration
from sports.annotators.soccer import draw_pitch
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mplsoccer import Pitch
import io
import os
import supervision as sv
from dotenv import load_dotenv
from prediction.view_transformer import ViewTransformer
import cv2

load_dotenv()

class Heatmap:
     def __init__(self, team_cluster):
        self.team_cluster = team_cluster
        self.file_name = os.getenv("TRACKED_FILE")
        self.model = YOLO(os.getenv("KEYPOINTS_MODEL"))
        self.pitch_config = SoccerPitchConfiguration()
        self.first_frame = cv2.imread(os.getenv("FIRST_FRAME_PATH"))

    
     def _get_bottom_center(self,bbox):
        x1, y1, x2, y2 = bbox
        x_center = (x1 + x2) / 2
        y_bottom = y2
        return (x_center, y_bottom)

     def _detect_reference_points(self):
          result = self.model.predict(self.first_frame)
          key_points = sv.KeyPoints.from_ultralytics(result[0])
          filter = key_points.confidence[0] > 0.5

          pitch_reference_points = np.array(self.pitch_config.vertices)[filter]
          frame_reference_points = key_points.xy[0][filter]

          return pitch_reference_points, frame_reference_points
      
     def _read_data(self):
            with open(self.file_name, "r") as f:
                tracked_data = json.load(f) 
            return tracked_data

     
     def create_heatmap(self): 
        pitch_reference_points, frame_reference_points = self._detect_reference_points()
        view_transformer = ViewTransformer(
             source=frame_reference_points,
             target=pitch_reference_points
        )

        tracked_data = self._read_data()

        team = [player for player in tracked_data['player'] if player['team'] == self.team_cluster]
        frame_players_xy = [self._get_bottom_center(player['bbox']) for player in team]
        pitch_players_xy = view_transformer.transform_points(np.array(frame_players_xy))

        pitch = draw_pitch(self.pitch_config)
        x, y = pitch_players_xy[:, 0], pitch_players_xy[:, 1]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.imshow(pitch, extent=[0, self.pitch_config.length, 0, self.pitch_config.width])

        sns.kdeplot(
            x=x,
            y=y,
            cmap="hot",
            fill=True,
            thresh=0.05,
            alpha=0.5,
            clip=((0, self.pitch_config.length), (0, self.pitch_config.width)),
            bw_adjust=1,
        )
        ax.set_aspect('equal')
        plt.tight_layout()
        plt.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
        buf.seek(0)
        plt.close()
        

        return buf
