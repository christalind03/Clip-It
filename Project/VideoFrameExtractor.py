import numpy
import uuid
import cv2
import os

def retrieve_timestamps_to_save(video_capture, num_frames_to_save):
    timestamps_to_save = []
    video_duration = video_capture.get(cv2.CAP_PROP_FRAME_COUNT) / video_capture.get(cv2.CAP_PROP_FPS)

    # Save all the timestamps to save a frame as specified by the "num_frames_to_save" parameter
    for iteration in numpy.arange(0, video_duration, 1 / num_frames_to_save):
        timestamps_to_save.append(iteration)

    return timestamps_to_save

def extract_frames(video_file):
    # Make a folder for the extracted frames if not made already
    if not os.path.isdir("Extracted Frames"):
        os.mkdir("Extracted Frames")

    video_capture = cv2.VideoCapture(video_file)
    fps = video_capture.get(cv2.CAP_PROP_FPS)

    timestamps_to_save = retrieve_timestamps_to_save(video_capture, 0.2) # Save 1 frame every 5 seconds
    frame_count = 0

    while True:
        is_read, current_frame = video_capture.read()

        if not is_read:
            break

        current_timestamp = frame_count / fps

        try:
            closest_timestamp_to_save = timestamps_to_save[0]
        except IndexError:
            break

        if current_timestamp >= closest_timestamp_to_save:
            cv2.imwrite(os.path.join("Extracted Frames", f"{str(uuid.uuid4())}.jpg"), current_frame)

            try:
                timestamps_to_save.pop(0)
            except IndexError:
                pass

        frame_count += 1

if __name__ == "__main__":
    import sys

    video_file = sys.argv[1]
    extract_frames(video_file)