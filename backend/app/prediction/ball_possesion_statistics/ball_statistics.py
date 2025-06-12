import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


class BallStatistics:
    def __init__(self, players_data):
        self.players = players_data

    def _get_players_with_ball_possession(self):
        seen_ids = set()
        unique_players = []
        for player in self.players:
            if player['has_ball'] and player['tracker_id'] not in seen_ids:
                unique_players.append(player)
                seen_ids.add(player['tracker_id'])
        return unique_players

    def _get_labels_(self):
        players_with_possession = self._get_players_with_ball_possession()
        labels = [player['team'] for player in players_with_possession]
        return labels

    def calculate_statistics_possesion(self):
        labels = self._get_labels_()
        unique_labels = list(set(labels))
        count_first_team = labels.count(unique_labels[0])
        count_second_team = labels.count(unique_labels[1])
        percentage_first_label = int(np.round((count_first_team / len(labels)) * 100))
        percentage_second_label = int(np.round((count_second_team / len(labels)) * 100))

        return percentage_first_label, percentage_second_label, count_first_team, count_second_team
