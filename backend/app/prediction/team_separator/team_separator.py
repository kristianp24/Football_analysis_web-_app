from .kmeans_performer import KMeansPerformer
from .colour_getter import ColourGetter
class TeamSeparator:
    def __init__(self, tracked_data):
        self.data = tracked_data
        self.colours = None
        self.labels = None
        self.centers = None
        self._get_colours_()
        self._get_labels_()

    def _get_colours_(self):
        colour_getter = ColourGetter(self.data)
        self.colours = colour_getter.get_colours()

    def _get_labels_(self):
        kmeans_model = KMeansPerformer(self.colours)
        self.labels, self.centers = kmeans_model.perform_KMeans()

    def separate_teams(self):
        modified_players = []
        for i, player in enumerate(self.data['player']):
            player['team'] = int(self.labels[i])
            modified_players.append(player)

        self.data['player'] = modified_players
        return self.data, self.centers
