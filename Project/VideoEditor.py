import os
import uuid
import ffmpeg
import datetime

from VideoAnalyzer import VideoAnalyzer

class VideoEditor:
    def __init__(self):
        self.video_analyzer = VideoAnalyzer()

    def trim_clip(self, input_file, output_file, start_time, end_time):
        # If the output file already exists, replace it
        if os.path.exists(output_file):
            os.remove(output_file)

        video_information = ffmpeg.probe(input_file)
        video_duration = video_information.get("format", {}).get("duration", None)

        input_stream = ffmpeg.input(input_file)

        video = input_stream.trim(start=start_time, end=end_time).setpts("PTS-STARTPTS")
        audio = (input_stream.filter_("atrim", start=start_time, end=end_time).filter_("apts", "PTS-STARTPTS"))
        video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)

        output = ffmpeg.output(video_and_audio, output_file, format="mp4")
        output.run()

    def generate_files(self, file_path, folder_path, track_round_start, track_spike_plant, record_event_type, record_min_kills, time_clipped_before, time_clipped_after):
        all_round_data = self.video_analyzer.analyze(file_path, int(record_min_kills))