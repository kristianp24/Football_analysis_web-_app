from prediction.pass_counter.check_bbox_diff import is_same_player
from prediction.pass_counter.ball_linear_movement import compute_angles
import pandas as pd
import numpy as np
from scipy.stats import zscore
class BallPassController:
    def __init__(self, valid_bboxes, nr_frames, players_data):
        self.valid_bboxes = valid_bboxes
        self.nr_frames = nr_frames
        self.players_data = players_data
        self.last_player = {}
        self.outliers = []

    def get_corrected_valid_bboxes(self):
        for nr in range(self.nr_frames):
            current_player = [player for player in self.players_data if player["frame_number"] == nr and player['has_ball']]
            if not current_player:
                continue
            if not self.last_player:
                self.last_player = current_player[0]
                continue

            if is_same_player(self.last_player['bbox'], current_player[0]['bbox']):
                continue

            if current_player[0]['tracker_id'] == self.last_player['tracker_id']:
                continue

            ball_bboxes = [self.valid_bboxes[i] for i in range(current_player[0]['frame_number'] + 1) if
                           self.last_player['frame_number'] <= i <= current_player[0]['frame_number']]

            self._correct_ball_linear_movement(current_player[0]['frame_number'], self.last_player['frame_number'], ball_bboxes)

        self._correct_bboxes()
        return self.valid_bboxes

    def _correct_bboxes(self):
        for frame in self.outliers:
            self.valid_bboxes[frame] = None


    def _correct_ball_linear_movement(self, current_frame, last_frame, ball_data):
        df = self._make_centers_df(current_frame, last_frame, ball_data)
        df = compute_angles(df)
        frame_outliers = self._get_outliers(df)
        for outlier in frame_outliers:
            self.outliers.append(outlier)
        # print(df)
        # print(frame_outliers)

    def _get_outliers(self, df, threshold=2):
        df["Angle_Z"] = np.abs(zscore(df["Angle"].fillna(0)))  # Compute Z-score
        df["X_Z"] = np.abs(zscore(df["X"].fillna(0)))
        df["Y_Z"] = np.abs(zscore(df["Y"].fillna(0)))

        df_outliers = df[
            (np.round(df["X_Z"]) >= threshold) |
            (np.round(df["Y_Z"]) >= threshold) |
            (np.round(df["Angle_Z"]) >= threshold)
            ]
        outliers = df_outliers['Frame_nr'].tolist()
        return outliers

    def _make_centers_df(self, current_frame, last_frame, bboxes):
        frames = [i for i in range(last_frame, current_frame + 1)]
        centers = [((x1 + x2) / 2, (y1 + y2) / 2) if bbox is not None else (0, 0)
                   for bbox in bboxes
                   for x1, y1, x2, y2 in [bbox or (0, 0, 0, 0)]]

        df = pd.DataFrame(centers, columns=["X", "Y"])
        df['Frame_nr'] = frames
        df.drop(df[(df["X"] == 0) & (df["Y"] == 0)].index, inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df





