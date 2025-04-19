import numpy as np
from collections import deque
from .set_last_player import set_last_player
from .check_bbox_diff import is_same_player
from .ball_linear_movement import is_ball_linear_movement
from .get_frames_indexes import get_frame_indexes
class PassCounter:
    def __init__(self, nr_frames: int, tracked_data):
        self.nr_frames = nr_frames
        self.tracked_data = tracked_data
        self.last_player = {}
        self.ball_bboxes = deque(maxlen=10)
        self.team_0_passes_counter = 0
        self.team_1_passes_counter = 0
        self.team_0_wrong_passes_counter = 0
        self.team_1_wrong_passes_counter = 0

    def get_number_of_passes(self):
        for i in range(self.nr_frames):
            ball = [ball for ball in self.tracked_data['ball'] if ball['frame_number'] == i]

            if ball is None:
                continue

            players = [player for player in self.tracked_data['player'] if player['frame_number'] == i and player['has_ball']]
            if not players:
                continue

            current_player = players[0]

            if not current_player:
                continue

            if not self.last_player:
                self.last_player = set_last_player(current_player)

            if self.last_player['tracker_id'] == current_player['tracker_id']:
                self.last_player = current_player
                continue

            if is_same_player(self.last_player['bbox'], current_player['bbox']):
                self.last_player = current_player
                continue

            if current_player['team'] != self.last_player['team']:
                self.last_player = current_player
                continue

            frame_last, frame_current = get_frame_indexes(self.tracked_data['ball'], current_player, self.last_player)

            if is_ball_linear_movement(self.tracked_data['ball'], frame_last, frame_current):
                team = current_player['team']
                if team == 0:
                    self.team_0_passes_counter += 1
                else:
                    self.team_1_passes_counter += 1

                print(f'Player with id {self.last_player['tracker_id']} passed to {current_player['tracker_id']}')

            self.last_player = current_player

        return self.team_0_passes_counter, self.team_1_passes_counter
            

