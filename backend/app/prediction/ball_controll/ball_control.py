import json
from collections import deque
import numpy as np
import supervision as sv


class BallController:
    def __init__(self, buffer_size: int = 10):
        self.buffer = deque(maxlen=buffer_size)
      

    def _get_centers(self, bboxes):
        centers = []
        for bbox in bboxes:
            x1, y1, x2, y2 = bbox
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            centers.append([center_x, center_y])
        return centers

    def _track_ball(self, bboxes, players_data, frame):
        if len(bboxes) > 0:
            centers = self._get_centers(bboxes)
            centers = np.array(centers).reshape(-1, 2)
            self.buffer.append(centers)

            centroid = np.mean(np.concatenate(self.buffer), axis=0)
            distances = np.linalg.norm(centers - centroid, axis=1)
            index = np.argmin(distances)

            is_a_player = self._check_missrecognition(bboxes[index], players_data, frame)
            if is_a_player is True:
                return None

            return bboxes[index]

        return None

    def _check_missrecognition(self, ball_bbox, players_data, frame):
        x1_ball, y1_ball, x2_ball, y2_ball = ball_bbox
        ball_width = x2_ball - x1_ball
        ball_height = y2_ball - y1_ball

        players = [p for p in players_data if p['frame_number'] == frame]

        for player in players:
            x1_player, y1_player, x2_player, y2_player = player['bbox']
            player_width = x2_player - x1_player
            player_height = y2_player - y1_player

            if not (x2_ball < x1_player or x1_ball > x2_player or
                    y2_ball < y1_player or y1_ball > y2_player):

                aspect_ratio = max(ball_width, ball_height) / min(ball_width, ball_height)
                if aspect_ratio > 1.5: 
                    print(f"Rejected ball {ball_bbox} (Bad aspect ratio: {aspect_ratio}) -> Likely a foot")
                    return True
                foot_threshold = y2_player - (player_height * 0.2)  
                if y1_ball > foot_threshold:
                    print(f"Rejected ball {ball_bbox} (Too low in Player {player['bbox']}) -> Likely a foot")
                    return True

                outside_x_left = x1_ball < x1_player - (player_width * 0.05)  
                outside_x_right = x2_ball > x2_player + (player_width * 0.05)  
                if outside_x_left or outside_x_right:
                    print(f"Rejected ball {ball_bbox} (Partially outside Player {player['bbox']}) -> Likely a foot")
                    return True

        return False 

    def get_valid_ball_bboxes(self, no_frames, tracked_data):
        valid_bboxes = []
        for i in range(no_frames):
            bboxes = []
            ball_list = [ball for ball in tracked_data['ball'] if ball['frame_number'] == i]
            for ball in ball_list:
                bboxes.append(ball['bbox'])
            valid_bbox = self._track_ball(bboxes, tracked_data['player'], i)

            valid_bboxes.append(valid_bbox)
        return valid_bboxes
