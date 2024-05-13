"""This module is responsible for video and audio preprocessing."""
import os

from preprocess_utilities import (
    list_files,
    parse_arguments,
    process_and_concatenate_videos,
)
from tqdm import tqdm


def main() -> None:
    args = parse_arguments()
    video_input_folder = args.video_folder
    audio_output_folder = args.audio_folder

    if not os.path.exists(audio_output_folder):
        os.makedirs(audio_output_folder)

    video_format = "MXF"
    file_list = list_files(video_input_folder, video_format)
    grouped_files = {}

    # Group files by participant ID extracted from directory names
    for file in file_list:
        participant_id = os.path.basename(os.path.dirname(file))
        if participant_id not in grouped_files:
            grouped_files[participant_id] = []
        grouped_files[participant_id].append(file)

    for participant_id, files in tqdm(grouped_files.items(), desc="Processing Participant Files"):
        files.sort()  # Further ensure files are sorted if needed
        output_filename = f"{participant_id}_concatenated.wav"
        output_path = os.path.join(audio_output_folder, output_filename)
        process_and_concatenate_videos(files, output_path, 16000)

if __name__ == "__main__":
    main()

