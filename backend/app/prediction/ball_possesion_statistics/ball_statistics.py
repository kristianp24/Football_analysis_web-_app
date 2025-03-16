import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
class BallStatistics:
    def __init__(self, players_data):
        self.players = players_data

    def calculate_ball_percentage_possesion_per_team(self):
        players_df = self._create_players_dataframe()
        labels, centers = self._perform_KMeans(players_df)
        ball_percentages, centers = self._calculate_statistics_possesion(labels, centers)
        print(f"Team {centers[0]} has a percentage of ball possesion {np.round(ball_percentages[0])}")
        print(f"Team {centers[1]} has a percentage of ball possesion {np.round(ball_percentages[1])}")



    def _create_players_dataframe(self):
        players_with_ball_possesion = [player for player in self.players['player'] if player['has_ball']]
        # A dataframe with players bbox and colour
        dict_data = []
        for player in players_with_ball_possesion:
            dict_data.append({
                'bbox': player['bbox'],
                'colour': player['colour']
            })
        players_df = pd.DataFrame(data=dict_data, columns=['bbox', 'colour'])
        return players_df

    def _calculate_statistics_possesion(self, labels, centers):
        unique_labels = list(set(labels))
        percentage_first_label = (labels.count(unique_labels[0]) / len(labels)) * 100
        percentage_second_label = (labels.count(unique_labels[1]) / len(labels)) * 100

        return (percentage_first_label, percentage_second_label), centers


    def _perform_KMeans(self, players_df):
        colours = players_df.loc[:, 'colour']
        array_colours = np.array(colours.tolist())
        array_colours = array_colours.reshape(-1, 3)

        kmeans_model = KMeans(n_clusters=2, random_state=42)
        labels = list(kmeans_model.fit_predict(array_colours))
        centers = kmeans_model.cluster_centers_
        return labels, centers