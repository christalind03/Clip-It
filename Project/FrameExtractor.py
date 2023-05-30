import os
import cv2
import uuid

def extract_frames(file_path):
    video = cv2.VideoCapture(file_path)
    max_fps = video.get(cv2.CAP_PROP_FPS)

    frame_count = 0
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    while frame_count < total_frames:
        is_read, current_frame = video.read()

        # Extract the frame once per second
        if frame_count % (max_fps * 2) == 0:
            # self.all_frames.append(current_frame)
            cv2.imwrite(os.path.join("C:/Users/chris/Downloads/Extracted Frames", f"{uuid.uuid4()}.jpg"), current_frame)
        
        frame_count += 1

    video.release()

file_path = "D:/VOD"
all_files = os.listdir(file_path)

for video in all_files:
    extract_frames(f"{os.path.join(file_path)}/{video}")