import os
import cv2
import uuid
from ultralytics import YOLO

class ObjectDetector:
    model = YOLO("C:/Users/chris/Downloads/Clip-It/Project/VALORANT-UI-Detector.pt")
    all_class_names = model.names

    def detect_objects(self, frame):
        results = self.model.predict(source=frame, save=True, project="Detected Objects", name="Video")[0]
        detected_objects = [self.all_class_names[int(class_index)] for class_index in results.boxes.cls]

        return detected_objects
            
    def clear_dir(self):
        pass