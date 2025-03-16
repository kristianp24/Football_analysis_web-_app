import json
from collections import deque
import numpy as np
import supervision as sv


class BallController:
    def __init__(self, buffer_size: int = 10):
        self.buffer = deque(maxlen=buffer_size)
        self.bbox_buffer = deque(maxlen=buffer_size)
        self.last_velocity = np.array([0, 0, 0, 0])
        self.distance_limit = 100.0

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

            if len(self.bbox_buffer) > 0:
                last_bbox = np.array(self.bbox_buffer[-1])
                current_bbox = np.array(bboxes[index])

                if not np.array_equal(last_bbox, current_bbox):
                    self.last_velocity = current_bbox - last_bbox

                is_a_player = self._check_missrecognition(bboxes[index], players_data, frame)
                if is_a_player is True:
                    return None

            self.bbox_buffer.append(bboxes[index])
            # punerea limitei ??
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

            # 1️⃣ Check if the bounding boxes overlap
            if not (x2_ball < x1_player or x1_ball > x2_player or
                    y2_ball < y1_player or y1_ball > y2_player):

                # 2️⃣ Aspect Ratio Check (Ball should be almost square)
                aspect_ratio = max(ball_width, ball_height) / min(ball_width, ball_height)
                if aspect_ratio > 1.5:  # Elongated shape means it's likely a foot
                    print(f"Rejected ball {ball_bbox} (Bad aspect ratio: {aspect_ratio}) -> Likely a foot")
                    return True

                # 3️⃣ Check if the "ball" is near the player's lower edges (feet region)
                foot_threshold = y2_player - (player_height * 0.2)  # Bottom 20% of player bbox
                if y1_ball > foot_threshold:
                    print(f"Rejected ball {ball_bbox} (Too low in Player {player['bbox']}) -> Likely a foot")
                    return True

                # 4️⃣ Check if the "ball" extends significantly outside the player's bbox (Legs do this)
                outside_x_left = x1_ball < x1_player - (player_width * 0.05)  # Ball extends too much to the left
                outside_x_right = x2_ball > x2_player + (player_width * 0.05)  # Ball extends too much to the right
                if outside_x_left or outside_x_right:
                    print(f"Rejected ball {ball_bbox} (Partially outside Player {player['bbox']}) -> Likely a foot")
                    return True

        return False  # If it passes all checks, it's a real ball

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

    def _predict_position(self):
        if len(self.buffer) == 0:
            return None

        last_bbox = self.bbox_buffer[-1]  # Get last known bounding box
        predicted_bbox = last_bbox + self.last_velocity
        self.bbox_buffer.append(predicted_bbox)

        return predicted_bbox.tolist()
