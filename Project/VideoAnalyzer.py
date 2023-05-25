import os
import cv2
import math
import uuid
import numpy
import datetime

from ObjectDetector import ObjectDetector

class RoundData:
    def __init__(self):
        self.round_start = None
        self.round_end = None

        self.first_kill = None
        self.recent_kill = (None, None)

        self.spike_planted = (None, None)

class VideoAnalyzer:
    def __init__(self):
        self.object_detector = ObjectDetector()
        self.all_rounds = []

    def generate_timestamps_to_save(self, video_capture, num_frames_to_save):
        timestamps_to_save = []
        video_duration = video_capture.get(cv2.CAP_PROP_FRAME_COUNT) / video_capture.get(cv2.CAP_PROP_FPS)

        # Save all the timestamps to save a frame as specified by the "num_frames_to_save" parameter
        for iteration in numpy.arange(0, video_duration, 1 / num_frames_to_save):
            timestamps_to_save.append(iteration)

        return timestamps_to_save

    def analyze(self, file_path, folder_path, num_frames_to_save):
        # Make a folder for the extracted frames if not made already
        if not os.path.isdir(folder_path):
            os.mkdir(folder_path)

        video_capture = cv2.VideoCapture(file_path)
        fps = video_capture.get(cv2.CAP_PROP_FPS)

        timestamps_to_save = self.generate_timestamps_to_save(video_capture, num_frames_to_save)
        frame_count = 0

        while True:
            is_read, current_frame = video_capture.read()

            if not is_read:
                break

            try:
                closest_timestamp_to_save = timestamps_to_save[0]
            except IndexError:
                break

            current_timestamp = frame_count / fps

            if current_timestamp >= closest_timestamp_to_save:
                # cv2.imwrite(os.path.join(folder_path, f"{str(uuid.uuid4())}.jpg"), current_frame)
                detected_objects = self.object_detector.detect_objects(current_frame)
                print(detected_objects)

                try:
                    timestamps_to_save.pop(0)
                except IndexError:
                    pass

            frame_count += 1