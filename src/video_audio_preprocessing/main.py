"""This module is responsible for video and audio preprocessing."""
import os

from preprocess_utilities import (
    list_files,
    parse_arguments,
    process_and_concatenate_videos,
)
from tqdm import tqdm


def __main__() -> None:
    """Main function for video and audio preprocessing."""
    video_format = "MXF"
    args = parse_arguments()
    video_input_folder = args.video_folder
    audio_output_folder = args.audio_folder
    audio_format = "wav"
    target_sample_rate = 16000

    if not os.path.exists(audio_output_folder):
        os.makedirs(audio_output_folder)

    file_list = list_files(
        video_input_folder, video_format
    )  # list_file innately has nat sorting
    grouped_files = {}

    for file in file_list:
        participant_id = os.path.basename(file)[:7]  # change for external IDs
        if participant_id not in grouped_files:
            grouped_files[participant_id] = []
        grouped_files[participant_id].append(file)

    for participant_id, files in tqdm(
        grouped_files.items(), desc="Processing Participant Files"
    ):
        files.sort()  # Ensure the files are in the correct order if not already
        output_filename = f"{participant_id}_concatenated.{audio_format}"
        output_path = os.path.join(audio_output_folder, output_filename)
        process_and_concatenate_videos(files, output_path, target_sample_rate)


__main__()
