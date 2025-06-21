import math
import pandas as pd
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

class TeamKilometersEstimator:
    def __init__(self, no_frames, video_length):
        self.data = self._read_data() 
        self.no_frames = no_frames
        self.video_length = video_length
        self.max_speed = 10

    def _read_data(self):
        with open(os.getenv("KM_RUNNER_POINTS_PATH"), 'rb') as f:
            data = pickle.load(f)
        return data

    def find_kilometers_runned(self, team_cluster):
        max_speed = self.max_speed
        frame_duration = self.video_length / self.no_frames
        team = self.data['team_' + str(team_cluster)]
        dict_distances = {}

        for player_id, points in team.items():
            last_x, last_y = None, None
            distances = []

            for point in points:
                x, y = point
                if last_x is None:
                    last_x, last_y = x, y
                    continue
                dx = x - last_x
                dy = y - last_y
                dist = math.hypot(dx, dy)
                speed = dist / frame_duration
                if speed > max_speed:
                    continue
                distances.append(dist)
                last_x, last_y = x, y

            dict_distances[player_id] = sum(distances)

        sum_cm = round(sum(dict_distances.values()))
        sum_kilometers = round(sum_cm / 100000, 3)
        sum_meters = round(sum_cm / 100, 3)

        return sum_meters, sum_kilometers

