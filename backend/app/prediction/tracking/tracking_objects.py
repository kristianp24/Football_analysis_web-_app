import pandas as pd
from ultralytics import YOLO
import supervision as sv
import json
import os
import cv2
from .tracking_utils import TrackingUtils
import numpy as np
import pickle
import sys
from inference_sdk import InferenceHTTPClient
from dotenv import load_dotenv

# sys.path.append('./')
from prediction.colour_assignment import ColourAssignment

load_dotenv()


class Tracker:
    def __init__(self):
        self.model = YOLO(os.getenv("MODEL_PATH"))
        self.tracker = sv.ByteTrack(lost_track_buffer=40, minimum_matching_threshold=0.85, track_activation_threshold=0.35)
        self.colour_assignment = ColourAssignment()
        self.referee_colour = (0, 255, 255)
        self.goalkeeper_colour = (255, 0, 0)
        self.CLIENT = InferenceHTTPClient(
            api_url=os.getenv("API_URL"),
            api_key=os.getenv("API_KEY")
        )
        self.model_id = os.getenv("MODEL_ID")

    def frame_detection(self, frames):
        detections = []
        iteration = 20

        for i in range(0, len(frames), iteration):
            print('Detecting 20 frames... Frame no:', i)

            # detection = (self.CLIENT.infer(frames[i:i + iteration], self.model_id))
            detection = (self.model.predict(frames[i:i + iteration]))

            detections += detection

        return detections

    def track_objects(self, frames, video_name):
        tracked_data = TrackingUtils.read_tracked_data(os.getenv("TRACKED_FILE"))
        if tracked_data is not None:
            if tracked_data['video_name'] == video_name:
                print('Tracked data already exists')
                return tracked_data
            
        detected_frames = self.frame_detection(frames)

        # intializing a data structure to store the tracks
        tracked_data = {
            "player": [],
            "referees": [],
            "ball": [],
            "goalkeeper": []
        }

        for number, result in enumerate(detected_frames):
            # detections with supervision
            # supervision_detection = sv.Detections.from_inference(result)
            supervision_detection = sv.Detections.from_ultralytics(result)

            # getting detections with track
            detectons_with_track = self.tracker.update_with_detections(supervision_detection)

            for detection in detectons_with_track:
                print('Tracking frames...')
                bounding_box = detection[0]
                class_id = detection[3]
                tracker_id = detection[4]

                if detection[5]['class_name'] == 'player':
                    tracked_data = TrackingUtils.add_tracked_data(tracked_data, 'player', bounding_box, class_id,
                                                                  tracker_id, number)

                if detection[5]['class_name'] == 'referee':
                    tracked_data = TrackingUtils.add_tracked_data(tracked_data, 'referees', bounding_box,
                                                                  class_id, tracker_id, number)

                if detection[5]['class_name'] == 'goalkeeper':
                    tracked_data = TrackingUtils.add_tracked_data(tracked_data, 'goalkeeper', bounding_box,
                                                                  class_id, tracker_id, number)

            for detection in supervision_detection:
                bounding_box = detection[0]
                class_id = detection[3]

                if detection[5]['class_name'] == 'ball':
                    tracked_data = TrackingUtils.add_tracked_data(tracked_data, 'ball', bounding_box, class_id,
                                                                  1, number)
        
        tracked_data['video_name'] = video_name
        TrackingUtils.write_tracked_data(os.getenv("TRACKED_FILE"), tracked_data)
        print('Data saved in file!')

        return tracked_data

    def draw_annotations(self, frames, tracked_data, ball_list: list):

        output = []
        players_modified_data_with_colours = []

        for nr, frame in enumerate(frames):
            aux_frame = frame.copy()

            player_list = [player for player in tracked_data['player'] if player['frame_number'] == nr]
            referee_list = [referee for referee in tracked_data['referees'] if referee['frame_number'] == nr]
            goalkeeper_list = [goalkeeper for goalkeeper in tracked_data['goalkeeper'] if goalkeeper['frame_number'] == nr]
            print('Drawing ellipses and ids...')

            for player in player_list:
                x1, y1, x2, y2 = player['bbox']

                colour =  self.colour_assignment.get_colour(player['bbox'], frame)
                aux_frame = TrackingUtils.draw_ellipse(aux_frame, player['bbox'], colour)
                aux_frame = TrackingUtils.write_id(aux_frame, player['tracker_id'], player['bbox'], colour)
                if player['has_ball']:
                    aux_frame = TrackingUtils.draw_triangle(aux_frame, player['bbox'], colour=(0, 0, 255))
                player['colour'] = list(colour)
                players_modified_data_with_colours.append(player)

            for referee in referee_list:
                aux_frame = TrackingUtils.draw_ellipse(aux_frame, referee['bbox'], self.referee_colour)

            for goalkeeper in goalkeeper_list:
                aux_frame = TrackingUtils.draw_ellipse(aux_frame, goalkeeper['bbox'], self.goalkeeper_colour)

            if len(ball_list) > 0:
                bbox_ball = ball_list[nr]
                if bbox_ball is not None:
                    x1, y1, x2, y2 = bbox_ball
                    if isinstance(x1, str):
                        continue
                    aux_frame = TrackingUtils.draw_triangle(aux_frame, bbox_ball, colour=(255, 0, 0), object_type="ball")
                    cv2.rectangle(aux_frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), thickness=4)

            output.append(aux_frame)
        # with open('writed_video/teamdata.text', 'w') as file:
        #     file.write(team_data)
        for player in tracked_data['player']:
            for modified_player in players_modified_data_with_colours:
                if player['frame_number'] == modified_player['frame_number'] and player['tracker_id'] == modified_player['tracker_id']:
                    player['colour'] = modified_player['colour']

        # print(tracked_data)

        return output, tracked_data
