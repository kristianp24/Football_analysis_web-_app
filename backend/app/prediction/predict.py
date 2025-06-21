from .video_utils import VideoUtils
import json
import numpy as np
from .tracking import Tracker
from .ball_controll import BallController
from .team_ball_possesion import BallPossesion
import cv2
from .ball_possesion_statistics import BallStatistics
from .ball_controll import BallPassController
from .team_separator import TeamSeparator
from .pass_counter import PassCounter
from .team_kilometers_speed_estimator import TeamKilometersEstimator, estimate_avg_speed_per_player
from .track_pitch_keypoints import ReferencePointsProjector
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv
import os
load_dotenv()


def predict(VIDEO_PATH, videoName: str):
    path = VIDEO_PATH + '/' + videoName 
    
    duration, no_frames, video_frames = get_duration_frame_nr(path)  
    cv2.imwrite(os.getenv('FIRST_FRAME_PATH'), video_frames[0])

    print('Readed video')
    tracker = Tracker()
    
    print('Tracking objects')
    tracked_data = tracker.track_objects(video_frames, video_name=videoName)
    tracked_data ['video_name'] = videoName
    tracked_data = tracker.get_player_colours(tracked_data, video_frames)

    ball_controller = BallController()
    valid_bboxes_ball = ball_controller.get_valid_ball_bboxes(len(video_frames), tracked_data)

    ball_possesion = BallPossesion(tracked_data, valid_bboxes_ball)
    tracked_data = ball_possesion.set_possesions()

    team_separator = TeamSeparator(tracked_data)
    new_data, centers = team_separator.separate_teams()

    track_pitch_keypoints = ReferencePointsProjector(video_frames, tracked_data)
    track_pitch_keypoints.project_points()

    ball_statistics = BallStatistics(tracked_data['player'])
    percentage_1, percentage_2, count_1, count_2 = ball_statistics.calculate_statistics_possesion()

    pass_counter = PassCounter(len(video_frames), new_data)
    team_0_passes, team_1_passes = pass_counter.get_number_of_passes()

    team_kilometers_estimator = TeamKilometersEstimator(duration, no_frames)
    distance_meters_team_0, distance_km_team_0 = team_kilometers_estimator.find_kilometers_runned(0)
    avg_speed_per_player_team_0 = estimate_avg_speed_per_player(distance_meters_team_0, duration)

    distance_meters_team_1, distance_km_team_1 = team_kilometers_estimator.find_kilometers_runned(1)
    avg_speed_per_player_team_1 = estimate_avg_speed_per_player(distance_meters_team_1, duration)
     
    colour_team_0 = bgr_to_rgb(centers[0].tolist())
    colour_team_1 = bgr_to_rgb(centers[1].tolist())

    prediction_data = {
        'video_name': videoName,
        'team_0': {
            'percentage_possesion': int(percentage_1),
            'number_of_passes': int(team_0_passes),
            'possesion_count': int(count_1),
            'colour': colour_team_0,
            'km_runned': distance_km_team_0,
            'avg_speed_player': float(np.round(avg_speed_per_player_team_0, 3)),
            'name': 'NA'
        },
        'team_1': {
            'percentage_possesion': int(percentage_2),
            'number_of_passes': int(team_1_passes),
            'possesion_count': int(count_2),
            'colour': colour_team_1,
            'km_runned': distance_km_team_1,
            'avg_speed_player': float(np.round(avg_speed_per_player_team_1, 3)),
            'name': 'NA'
        },
    }
    
    with open(os.getenv("TRACKED_FILE"), "w") as f:
        json.dump(new_data, f)

    # VideoUtils.writeVideo(drawed_frames, os.getenv("PREDICTED_VIDEO_PATH"))
    print('Predicted video saved')
    return True, prediction_data
    

def bgr_to_rgb(bgr_colour):

    r = int(bgr_colour[2])
    g = int(bgr_colour[1])
    b = int(bgr_colour[0])
    return (r, g, b)

def get_duration_frame_nr(path):
    clip = VideoFileClip(path)
    duration = int(clip.duration)
    video_frames = VideoUtils.readVideo(path)
    no_frames = len(video_frames)   
    return duration, no_frames, video_frames
