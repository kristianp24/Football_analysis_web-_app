
def get_frame_indexes(ball_data, current_player, last_player):
    if last_player['frame_number'] < current_player['frame_number']:
        return int(last_player['frame_number']), int(current_player['frame_number'])