import os
import cv2
import time

from multiprocessing import Pool
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

        self.all_frames = []
        self.all_frame_data = []
        self.all_round_data = []

    def extract_frames(self, file_path):
        frame_count = 0
        video = cv2.VideoCapture(file_path)
        max_fps = video.get(cv2.CAP_PROP_FPS)

        while True:
            is_read, current_frame = video.read()

            if is_read:
                # Extract the frame once per second
                if frame_count % max_fps == 0:
                    self.all_frames.append(current_frame)
                
                frame_count += 1
                
            else:
                break

    def analyze(self, file_path):
        self.extract_frames(file_path)

        with Pool() as pool:
            frame_data = pool.imap(self.object_detector.detect_objects, self.all_frames)
            self.all_frame_data.append(frame_data)