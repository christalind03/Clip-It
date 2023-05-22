import VideoFrameExtractor

# need file path, folder path,
# get_round_start_timestamp, get_spike_plant_timestamp
# record_entire_round, record_kills_only, min_num_kills_to_record,
# time_clipped_before, time_clipped_after
def analyze(file_path, folder_path):
    VideoFrameExtractor.extract_frames(file_path, folder_path)