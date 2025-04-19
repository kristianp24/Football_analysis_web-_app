
def set_last_player(current_player: dict):
    last_player = {
        'tracker_id': current_player['tracker_id'],
        'bbox': current_player['bbox'],
        'team': current_player['team']
    }

    return last_player
