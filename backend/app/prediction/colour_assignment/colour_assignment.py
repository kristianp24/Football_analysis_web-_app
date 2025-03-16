import cv2
from sklearn.cluster import KMeans
import numpy as np

class ColourAssignment:
       
       def __init__(self):
              pass
       
       def get_colour(self,bbox, frame):
              top_half_image = self.crop_player(bbox, frame)
              data_2d = top_half_image.reshape((-1, 3))

              kmeans = KMeans(n_clusters=2, random_state=0)
              kmeans.fit(data_2d)
              labels = kmeans.labels_
              clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])
              background_cluster = clustered_image[0,0]
              player_cluster = 1-background_cluster
              rgb = kmeans.cluster_centers_[player_cluster]
              rgb_rounded = np.round(rgb, decimals=2)
              return rgb_rounded

       
       def crop_player(self,bbox, frame):
              x1, y1, x2, y2 = bbox
              image = frame[int(y1):int(y2), int(x1):int(x2)]
              top_half = image[:int(image.shape[0] / 2), :]

              return top_half
