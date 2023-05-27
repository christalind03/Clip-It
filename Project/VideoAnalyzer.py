import cv2
from ultralytics import YOLO

class RoundData:
    def __init__(self):
        self.round_start = None
        self.round_end = None

        self.first_kill = (False, None)
        self.recent_kill = None

        self.spike_planted = (False, None)

class VideoAnalyzer:
    model = YOLO("C:/Users/chris/Downloads/Clip-It/Project/VALORANT-UI-Detector.pt")
    all_class_names = model.names

    def __init__(self):
        self.all_frames = []
        self.all_frame_data = []
        self.all_round_data = []

    def extract_frames(self, file_path):
        frame_count = 0
        video = cv2.VideoCapture(file_path)
        max_fps = video.get(cv2.CAP_PROP_FPS)

        while True:
            is_read, current_frame = video.read()

            if not is_read:
                break

            # Extract the frame once per second
            if frame_count % max_fps == 0:
                self.all_frames.append(current_frame)
            
            frame_count += 1
    
    def detect_objects(self, frame):
        results = self.model.predict(source=frame)[0]
        detected_objects = [self.all_class_names[int(class_index)] for class_index in results.boxes.cls]

        return detected_objects

    def analyze(self, file_path, record_min_kills):
        self.extract_frames(file_path)

        # Analyze each frame
        for frame in self.all_frames:
            frame_data = self.detect_objects(frame)
            self.all_frame_data.append(frame_data)

        del self.all_frames

        # Use frame data to create round data
        current_round_data = None
        all_kill_types = {"kill-1", "kill-2", "kill-3", "kill-4", "kill-5", "kill-6"}

        for current_time, frame_data in enumerate(self.all_frame_data):
            # Get round start information
            if current_round_data is None and "round-start" in frame_data:
                current_round_data = RoundData()
                current_round_data.round_start = current_time

            # If there is current round data record the kills, spike plant, and round end times respectively
            if current_round_data is not None:
                kill_type = list(set(frame_data) & all_kill_types)

                if kill_type and "spectating" not in frame_data:
                    kill_count = int(kill_type[0][-1])

                    if not current_round_data.first_kill[0] and kill_count == record_min_kills:
                        current_round_data.first_kill = (True, current_time)
                        current_round_data.recent_kill = current_time

                    if kill_count > record_min_kills:
                        current_round_data.recent_kill = current_time

                if not current_round_data.spike_planted[0]:
                    current_round_data.spike_planted = (True, current_time)

                if "round-end" in frame_data:
                    current_round_data.round_end = current_time

                    self.all_round_data.append(current_round_data)
                    current_round_data = None

        del self.all_frame_data
        return self.all_round_data