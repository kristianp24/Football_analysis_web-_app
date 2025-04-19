
class ColourGetter:
    def __init__(self, tracked_data):
        self.data = tracked_data

    def get_colours(self):
        players_data = self.data['player']
        colours = [player['colour'] for player in players_data]
        return colours


