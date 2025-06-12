import math
import pandas as pd

class TeamKilometersEstimator:
    def __init__(self, data, no_frames, video_length):
        self.data = data
        self.no_frames = no_frames
        self.video_length = video_length
        self.max_speed = 10

    def _get_centre(self, bbox):
        x1, y1, x2, y2 = bbox
        cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2

        return cx1, cy1
   
    def _modify_team_data(self, team):
        modified_players = []
        for player in team:
            cx, cy = self._get_centre(player['bbox'])
            cx = (cx / 1920) * 105
            cy = (cy / 1080) * 68
            modified_players.append(
                {
                    'team': player['team'],
                    'center_x': cx,
                    'center_y': cy,
                    'frame': player['frame_number'],
                    'id': player['tracker_id']
                }
            )
        modified_players.sort(key=lambda m: m['frame'])

        return modified_players

    def _get_unique_ids(self, team_modified):
        unique_ids = {player['id'] for player in team_modified}
        unique_ids_list = list(unique_ids)

        return unique_ids_list

    def _interpolate_data(self, player_data):
        df = pd.DataFrame(player_data)
        df.set_index('frame', inplace=True)

        full_index = range(df.index.min(), df.index.max() + 1)
        df = df.reindex(full_index)

        df_interp = df[['center_x', 'center_y']].interpolate(method='linear')

        df_interp.reset_index(inplace=True)

        return df_interp

    def find_kilometers_runned(self, team_cluster):
        max_speed = self.max_speed
        frame_duration = self.video_length / self.no_frames
        team = [player for player in self.data['player'] if player['team'] == team_cluster]
        team_modified = self._modify_team_data(team)
        unique_ids = self._get_unique_ids(team_modified)
        dict_distances = {}

        for id in unique_ids:
            player = [p for p in team_modified if p['id'] == id]

            df_interpolated_player = self._interpolate_data(player)
            player2 = df_interpolated_player[['center_x', 'center_y']].to_dict(orient='records')

            last_positon_X = -1
            last_positon_Y = -1
            distances = []

            for player_position in player2:
                if last_positon_X == -1 or last_positon_Y == -1:
                    last_positon_X = player_position['center_x']
                    last_positon_Y = player_position['center_y']

                else:
                    dx = player_position['center_x'] - last_positon_X
                    dy = player_position['center_y'] - last_positon_Y

                    distance = math.hypot(dx, dy)
                    speed = distance / frame_duration
                    if speed > max_speed:
                        continue
                    # if distance < 0.1:
                    #     continue
                    distances.append(distance)
                    last_positon_X = player_position['center_x']
                    last_positon_Y = player_position['center_y']

            dict_distances[str(id)] = sum(distances)

        sum_meters = sum(dict_distances.values())
        sum_kilometers = round(sum_meters / 1000, 3)
        sum_meters = round(sum_meters)

        return sum_meters, sum_kilometers





