import os
import cv2
import easyocr
from ultralytics import YOLO

class ObjectDetector:
    model = YOLO("C:\\Users\\chris\\Downloads\\Clip-It\\Project\\VALORANT-UI-Detector.pt")
    all_class_names = model.names

    def detect_objects(self, frame):
        results = self.model.predict(source=frame, save_crop=True, project="Detected Objects")[0]
        detected_objects = results.boxes.cls

        return [self.all_class_names[int(class_index)] for class_index in detected_objects]