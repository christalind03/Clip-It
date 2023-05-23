import VideoFrameExtractor

def analyze(file_path, folder_path):
    num_frames_to_save = 1
    VideoFrameExtractor.extract_frames(file_path, folder_path, num_frames_to_save)