def estimate_avg_speed_per_player(meters_team, no_seconds, no_players=11):
    avg_speed_per_player = meters_team / (no_players * no_seconds)
    avg_speed_per_player = avg_speed_per_player * 3.6  
    return avg_speed_per_player
