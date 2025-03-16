from .video_utils import VideoUtils
import json
import os
from .tracking import Tracker
from .ball_controll import BallController
from .team_ball_possesion import BallPossesion
import cv2
from .ball_possesion_statistics import BallStatistics


def predict(VIDEO_PATH, videoName: str):
    path = VIDEO_PATH + '/' + videoName 
    print(path)
    video_frames = VideoUtils.readVideo(path)
    print(len(video_frames))
    print('Readed video')
    tracker = Tracker('C:/Users/HP/OneDrive/Desktop/football_analysys_web_app/backend/app/prediction/model/weights_v9.pt')
    tracked_file = 'tracked_' + videoName + '.json'
    print('Tracking objects')
    tracked_data = tracker.track_objects(video_frames, tracked_file)

    ball_controller = BallController()
    valid_bboxes_ball = ball_controller.get_valid_ball_bboxes(len(video_frames), tracked_data)

    ball_possesion = BallPossesion(tracked_data, valid_bboxes_ball)
    tracked_data = ball_possesion.set_possesions()

    print('Drawing annotations')    
    drawed_frames, tracked_data = tracker.draw_annotations(video_frames, tracked_data, valid_bboxes_ball)

    with open("modified_players_data.json", "w") as f:
        json.dump(tracked_data, f)
    VideoUtils.writeVideo(drawed_frames, 'predicted/tracked_with_v9.avi')
    print('Predicted video saved')
    return True
    # print(players_data)
    # ball_statistics = BallStatistics(tracked_data)
    # ball_statistics.calculate_ball_percentage_possesion_per_team()
