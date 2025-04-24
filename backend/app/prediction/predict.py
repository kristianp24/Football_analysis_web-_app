from .video_utils import VideoUtils
import json
import os
from .tracking import Tracker
from .ball_controll import BallController
from .team_ball_possesion import BallPossesion
import cv2
from .ball_possesion_statistics import BallStatistics
from .ball_controll import BallPassController
from .team_separator import TeamSeparator
from .pass_counter import PassCounter

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

    ball_pass_controller = BallPassController(valid_bboxes_ball, len(video_frames), tracked_data['player'])
    valid_bboxes_ball2 = ball_pass_controller.get_corrected_valid_bboxes()

    print('Drawing annotations')    
    drawed_frames, tracked_data = tracker.draw_annotations(video_frames, tracked_data, valid_bboxes_ball)

    team_separator = TeamSeparator(tracked_data)
    new_data, centers = team_separator.separate_teams()

    ball_statistics = BallStatistics(tracked_data['player'])
    percentage_1, percentage_2, count_1, count_2 = ball_statistics.calculate_statistics_possesion()

    pass_counter = PassCounter(len(video_frames), new_data)
    team_0_passes, team_1_passes = pass_counter.get_number_of_passes()
     
    colour_team_0 = bgr_to_rgb(centers[0].tolist())
    colour_team_1 = bgr_to_rgb(centers[1].tolist())

    prediction_data ={
        'video_name': videoName,
        'team_0': {
            'percentage_possesion': int(percentage_1),
            'number_of_passes': int(team_0_passes),
            'possesion_count': int(count_1),
            'colour': colour_team_0,
            'name': 'NA'
        },
        'team_1': {
            'percentage_possesion': int(percentage_2),
            'number_of_passes': int(team_1_passes),
            'possesion_count': int(count_2),
            'colour': colour_team_1,
            'name': 'NA'
        },
    }
    print(prediction_data)
    



    # with open("modified_players_data.json", "w") as f:
    #     json.dump(tracked_data, f)
    # VideoUtils.writeVideo(drawed_frames, 'predicted_video/tracked_with_v9.avi')
    print('Predicted video saved')
    return True, prediction_data
    # print(players_data)
    # ball_statistics = BallStatistics(tracked_data)
    # ball_statistics.calculate_ball_percentage_possesion_per_team()

def bgr_to_rgb(bgr_colour):
    r = int(bgr_colour[2])
    g = int(bgr_colour[1])
    b = int(bgr_colour[0])
    return (r, g, b)
