import supervision as sv
import numpy as np
from prediction.view_transformer import ViewTransformer
from sports.configs.soccer import SoccerPitchConfiguration
import json
from ultralytics import YOLO
import os
import pickle
from dotenv import load_dotenv
from collections import defaultdict
load_dotenv()

class ReferencePointsTracker:
    def __init__(self, frames, tracked_data):
        self.model = YOLO(os.getenv("MODEL"))
        self.frames = frames
        self.frame_count = len(frames)
        self.tracked_data = tracked_data
        self.pitch_config = SoccerPitchConfiguration()
        self.team_cluster = [0, 1]
        self.dict_km_runner_points = defaultdict(lambda: defaultdict(list))
        self.projected_points_file = os.getenv("PROJECTED_POINTS_PATH")
    
    def _get_bottom_center(self, bbox):
        x1, y1, x2, y2 = bbox
        x_center = (x1 + x2) / 2
        y_bottom = y2
        return (x_center, y_bottom)
    
    def _detect_reference_points(self, frame):
        result = self.model.predict(frame)
        key_points = sv.KeyPoints.from_ultralytics(result[0])
        mask = key_points.confidence[0] > 0.5

        pitch_reference_points = np.array(self.pitch_config.vertices)[mask]
        frame_reference_points = key_points.xy[0][mask]

        return pitch_reference_points, frame_reference_points
    
    def _set_km_runner_points(self, view_transformer, players):
        for player in players:
            team = "team_" + str(player['team'])
            self.dict_km_runner_points[team][player['tracker_id']].append(
                view_transformer.transform_points(
                    np.array(self._get_bottom_center(player['bbox']))).tolist()[0]
            )

    def _save_km_runner_points(self):
        clean_dict = {
            team: dict(players)
            for team, players in self.dict_km_runner_points.items()
        }
        print(clean_dict['team_0'])
        with open(os.getenv("KM_RUNNER_POINTS_PATH"), 'wb') as f:
            pickle.dump(clean_dict, f)
        print('KM runner points saved to:', os.getenv("KM_RUNNER_POINTS_PATH"))
    
    def _save_all_projected_points(self, dict_projected_points):
        with open(self.projected_points_file, 'w') as f:
            json.dump(dict_projected_points, f, indent=2)
        print('Projected points saved ')

    def project_points(self):

        dict_projected_points = {
            'team_0': [],
            'team_1': []
        }
        all_projected_points = []
        
        for cluster in self.team_cluster:
            all_projected_points = []
            for idx in range(0, self.frame_count, 10):
               
                frame = self.frames[idx]
                print('A intrat in bucla')
                try:
                    pitch_ref, frame_ref = self._detect_reference_points(frame)
                    view_transformer = ViewTransformer(source=frame_ref, target=pitch_ref)

                except Exception as e:
                    print(f"Eroare detectare puncte la frame {idx}: {e}")
                    continue

                players = [p for p in self.tracked_data['player'] if p['team'] == cluster and p['frame_number'] == idx]
                frame_players_xy = [self._get_bottom_center(p['bbox']) for p in players]
                if not frame_players_xy:
                    continue

                projected = view_transformer.transform_points(np.array(frame_players_xy))
                self._set_km_runner_points(view_transformer, players)
                all_projected_points.extend(projected.tolist())
            dict_projected_points[f'team_{cluster}'] = all_projected_points
        
        self._save_all_projected_points(dict_projected_points)
        self._save_km_runner_points()
    