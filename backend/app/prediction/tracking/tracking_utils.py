import os
import json
import cv2
import numpy as np


class TrackingUtils:

    @staticmethod
    def draw_triangle(aux_frame, bbox, colour, object_type="player"):
        x1, y1, x2, y2 = bbox
        triangle_height = 8  # Adjust this to change the triangle height
        triangle_width_factor = 0.5  # Controls how wide the triangle is
        if object_type == "ball":
            triangle_width_factor = 0.7

        # Calculate triangle vertices
        top = ((x1 + x2) // 2, y1)  # Point inside the bbox
        left = (x1 + int((x2 - x1) * (1 - triangle_width_factor) / 2), y1 - triangle_height)  # Shrink width
        right = (x2 - int((x2 - x1) * (1 - triangle_width_factor) / 2), y1 - triangle_height)
        triangle_pts = np.array([top, left, right], np.int32)
        triangle_pts = triangle_pts.reshape((-1, 1, 2))
        cv2.fillPoly(aux_frame, [triangle_pts], color=colour, lineType=cv2.LINE_AA)
        return aux_frame

    @staticmethod
    def add_tracked_data(tracked_data: dict[str, list], object_detected: str, bbox, class_id, tracker_id, frame_number):
        tracked_data[object_detected].append({
            "bbox": bbox.tolist(),
            "class_id": int(class_id),
            "tracker_id": int(tracker_id),
            "frame_number": frame_number
        })
        return tracked_data

    @staticmethod
    def read_tracked_data(path_to_json):
        if os.path.exists(path_to_json):
            with open(path_to_json, "r") as file:
                return json.load(file)
        return None

    @staticmethod
    def write_tracked_data(path_to_json, tracked_data):
        with open(path_to_json, "w") as file:
            json.dump(tracked_data, file)

    @staticmethod
    def write_id(frame, id, bbox, color):
        x1, y1, x2, y2 = bbox

        # cv2.rectangle(frame, (int(x1 + 0.01 * x1), int(y1 + 0.07 * y1)), (int(x2 - 0.01 * x2), int(y2 + y2 * 0.03)),
        #               color, thickness=2)

        cx = int((x1 + 0.01 * x1 + x2 - 0.01 * x2) / 2)
        cy = int((y1 + 0.07 * y1 + y2 + y2 * 0.03) / 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(str(id), font, font_scale,
                                                              thickness)
        text_x = cx - text_width // 2
        text_y = cy + text_height // 2
        cv2.putText(frame, str(id), (text_x, text_y), fontFace=font, fontScale=font_scale,
                    thickness=thickness, color=(0, 0, 0))

        # frame = self.draw_rectangle(frame, bbox, id)

        return frame

    @staticmethod
    def draw_ellipse(aux_frame, bbox, colour):
        x1, y1, x2, y2 = bbox
        center_x = int((x1 + x2) / 2)
        width = x2 - x1
        cv2.ellipse(
            aux_frame,
            center=(center_x, int(y2)),
            axes=(int(width), int(0.4 * width)),
            angle=0.0,
            startAngle=-40,
            endAngle=260,
            color=colour,
            thickness=2,
            lineType=cv2.LINE_AA
        )
        return aux_frame

    @staticmethod
    def set_teams_data(teams_data: dict, players_data: list, frame_number: int):
        teams_data[frame_number] = {'players': players_data}
        return teams_data

    def draw_rectangle(self, frame, bbox, id):
        x1, y1, x2, y2 = bbox
        # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), thickness=2)
        cv2.rectangle(frame, (int(x1 + 0.01 * x1), int(y1 + 0.07 * y1)), (int(x2 - 0.01 * x2), int(y2 + y2 * 0.03)),
                      (0, 255, 0), thickness=2)

        return frame
