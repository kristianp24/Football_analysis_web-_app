import cv2


class VideoUtils:
    @staticmethod
    def readVideo(path):
        input_video = cv2.VideoCapture(path)
        frames = []
        while input_video.isOpened():
            flag, frame = input_video.read()
            if not flag:
                break
            frames.append(frame)

        return frames

    @staticmethod
    def writeVideo(frames, output_path):
        codec = cv2.VideoWriter.fourcc(*'XVID')
        video = cv2.VideoWriter(output_path, codec, 24, (frames[0].shape[1], frames[0].shape[0]))

        for frame in frames:
            video.write(frame)
        video.release()
