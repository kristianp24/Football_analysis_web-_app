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
from .track_pitch_keypoints import ReferencePointsTracker
from moviepy.video.io.VideoFileClip import VideoFileClip
from dotenv import load_dotenv
import os
load_dotenv()

def is_false_ball_detection(ball_box, player_box, proximity_threshold=20):
    """
    Returns True if the ball detection is likely a false positive:
    very close to player's feet AND inside the player bbox.
    
    :param ball_box: Tuple (x1, y1, x2, y2) for the ball
    :param player_box: Tuple (x1, y1, x2, y2) for the player
    :param proximity_threshold: Distance in pixels to feet below which it's suspicious
    :return: True if it should be filtered out, False otherwise
    """
    import math

    def center(box):
        x1, y1, x2, y2 = box
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def feet_position(box):
        x1, y1, x2, y2 = box
        return ((x1 + x2) // 2, y2)

    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def is_inside(inner, outer):
        ix1, iy1, ix2, iy2 = inner
        ox1, oy1, ox2, oy2 = outer
        return ix1 >= ox1 and iy1 >= oy1 and ix2 <= ox2 and iy2 <= oy2

    ball_center = center(ball_box)
    player_feet = feet_position(player_box)

    if distance(ball_center, player_feet) < proximity_threshold and is_inside(ball_box, player_box):
        return True  # This is a likely false detection
    return False  # This is likely a valid ball




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

    track_pitch_keypoints = ReferencePointsTracker(video_frames, tracked_data)
    track_pitch_keypoints.track()

    ball_statistics = BallStatistics(tracked_data['player'])
    percentage_1, percentage_2, count_1, count_2 = ball_statistics.calculate_statistics_possesion()

    pass_counter = PassCounter(len(video_frames), new_data)
    team_0_passes, team_1_passes = pass_counter.get_number_of_passes()

    team_kilometers_estimator = TeamKilometersEstimator(tracked_data, duration, no_frames)
    distance_meters_team_0, distance_km_team_0 = team_kilometers_estimator.find_kilometers_runned(0)
    avg_speed_per_player_team_0= estimate_avg_speed_per_player(distance_meters_team_0, duration)

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
    print(prediction_data)
    
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
