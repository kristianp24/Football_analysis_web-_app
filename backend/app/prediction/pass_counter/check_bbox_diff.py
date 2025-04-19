import math


def is_same_player(last_player_bbox, current_player_bbox, distance_threshold=40):
    x1, y1, x2, y2 = last_player_bbox
    x1p, y1p, x2p, y2p = current_player_bbox

    cx1, cy1 = (x1 + x2) / 2, (y1 + y2) / 2
    cx2, cy2 = (x1p + x2p) / 2, (y1p + y2p) / 2

    distance = math.sqrt((cx1 - cx2) ** 2 + (cy1 - cy2) ** 2)

    return distance <= distance_threshold
