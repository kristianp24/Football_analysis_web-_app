from collections import Counter
from sklearn.cluster import KMeans
import numpy as np
import math


class BallPossesion:
    def __init__(self, tracked_data, ball_data):
        self.tracked_data = tracked_data
        self.ball_data = ball_data
        self.has_ball = True
        self.do_not_have_ball = False
        self.threshold = 55
        self.min_distance = 99999

    def _get_goalkeeper(self):
        goalkeeper_list = self.tracked_data['goalkeeper']
        goalkeeper = goalkeeper_list[0]

    def set_possesions(self):
        players_modified_data_with_ball_assignment = []
        # frames_ball_in_air = frames_where_ball_in_air(self.ball_data)
        print('Setting possesions...')
        print('len ball data: ', len(self.ball_data))
        for i, ball_bbox in enumerate(self.ball_data):
            players_data = [player for player in self.tracked_data['player'] if player['frame_number'] == i]

            self.min_distance = 9999
            assigned_ball = False
            for player in players_data:
                if ball_bbox is not None:
                    assigned_ball = self._ball_assignment_(bbox_player=player['bbox'], bbox_ball=ball_bbox)
                    player['has_ball'] = self.has_ball if (assigned_ball
                                                           and self._is_ball_at_player_legs(ball_bbox, player['bbox'])) \
                        else self.do_not_have_ball
                    # player['has_ball'] = self.has_ball if assigned_ball else self.do_not_have_ball
                else:
                    player['has_ball'] = self.do_not_have_ball

                players_modified_data_with_ball_assignment.append(player)

        for player in self.tracked_data['player']:
            for modified_player in players_modified_data_with_ball_assignment:
                if player['frame_number'] == modified_player['frame_number'] and player['tracker_id'] == \
                        modified_player['tracker_id']:
                    player['has_ball'] = modified_player['has_ball']

        return self.tracked_data

    def _is_ball_at_player_legs(self, bbox_ball, bbox_player, belly_ratio = 0.4):
        x_pmin, y_pmin, x_pmax, y_pmax = bbox_player
        x_bmin, y_bmin, x_bmax, y_bmax = bbox_ball

        # belly-to-legs region
        y_belly = y_pmin + belly_ratio * (y_pmax - y_pmin)

        y_overlap = (y_bmax > y_belly) and (y_bmin > y_belly) and (y_bmin < y_pmax)

        return y_overlap



    def _get_bbox_center(self, bbox):
        x_min, y_min, x_max, y_max = bbox

        return int((x_min + x_max) / 2), int((y_min + y_max) / 2)

    def distance_between_points(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def _ball_assignment_(self, bbox_player: list, bbox_ball: list):
        ball_center_x, ball_center_y = self._get_bbox_center(bbox_ball)

        assigned_player = -2

        left_distance = self.distance_between_points(bbox_player[0], bbox_player[-1], ball_center_x, ball_center_y)
        right_distance = self.distance_between_points(bbox_player[2], bbox_player[-1], ball_center_x, ball_center_y)
        distance = min(right_distance, left_distance)

        if distance < self.threshold:
            if distance < self.min_distance:
                self.min_distance = distance
                return True
        return False
