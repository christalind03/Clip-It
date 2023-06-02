import os
import ffmpeg

from datetime import timedelta
from VideoAnalyzer import VideoAnalyzer

class VideoEditor:
    def __init__(self):
        self.video_analyzer = VideoAnalyzer()

    def trim_video(self, input_stream, output_file, start_time, end_time):
        # If the output file already exists, replace it
        if os.path.exists(output_file):
            os.remove(output_file)

        video = input_stream.trim(start=start_time, end=end_time).setpts("PTS-STARTPTS")
        audio = (input_stream.filter_("atrim", start=start_time, end=end_time).filter_("asetpts", "PTS-STARTPTS"))
        video_and_audio = ffmpeg.concat(video, audio, v=1, a=1)

        output = ffmpeg.output(video_and_audio, output_file, format="mp4")
        output.run()

    def generate_files(self, file_path, folder_path, track_round_start, track_spike_plant, record_event_type, record_min_kills, time_clipped_before, time_clipped_after):        
        file_name = file_path.split("/")[-1].split(".")[0]
        all_round_data = self.video_analyzer.analyze(file_path)

        # Record events via timestamp
        if track_round_start or track_spike_plant:
            all_timestamps = open(os.path.join(folder_path, f"{file_name} Timestamps.txt"), "w")
        
            def create_timestamp(seconds):
                return str(timedelta(seconds=seconds))

            for number, round_data in enumerate(all_round_data, start=1):
                if track_round_start:
                    all_timestamps.write(f"{create_timestamp(round_data.round_start)} - Round {number}\n")
                
                if track_spike_plant and round_data.spike_planted[1] is not None:
                    all_timestamps.write(f"{create_timestamp(round_data.spike_planted[1])} - Round {number} Postplant\n")

            all_timestamps.close()

        # Record events via clips
        if record_event_type:
            # Prepare original video for trimming
            video_information = ffmpeg.probe(file_path)
            video_duration = video_information.get("format", {}).get("duration", None)
            input_stream = ffmpeg.input(file_path)

            if record_event_type == "ROUND":
                for round_number, round_data in enumerate(all_round_data, start=1):
                    output_flie = os.path.join(folder_path, f"{file_name} - Round {round_number}.mp4")
                    self.trim_video(input_stream, output_file, round_data.round_start, round_data.round_end)

            if record_event_type == "KILLS":
                clip_number = 1

                for round_data in all_round_data:
                    kill_count = round_data.recent_kill[0]

                    if kill_count and kill_count >= record_min_kills:
                        output_file = os.path.join(folder_path, f"{file_name} - Clip {clip_number}.mp4")
                        start_clip = round_data.first_kill[1] - time_clipped_before
                        end_clip = round_data.recent_kill[1] + time_clipped_after

                        self.trim_video(input_stream, output_file, start_clip, end_clip)
                        clip_number += 1