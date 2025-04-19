import numpy as np
from sklearn.cluster import KMeans

class KMeansPerformer:
    def __init__(self, colours):
        self.colours = colours

    def perform_KMeans(self):
        colours = self.colours
        array_colours = np.array(colours)
        array_colours = array_colours.reshape(-1, 3)

        kmeans_model = KMeans(n_clusters=2, random_state=42)
        labels = list(kmeans_model.fit_predict(array_colours))
        centers = kmeans_model.cluster_centers_
        return labels, centers
