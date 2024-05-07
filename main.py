from preprocess_utilities import list_files, process_and_concatenate_videos
import os
from tqdm import tqdm


def __main__():
    video_format = "MXF"
    video_input_folder = "/Users/celia.maiorano/Python_Repositories/semantic_sommeliers/Video-Audio_Preprocessing/data/videos"
    audio_output_folder = "/Users/celia.maiorano/Python_Repositories/semantic_sommeliers/Video-Audio_Preprocessing/data/audios"
    audio_format = "wav"
    target_sample_rate = 16000

    if not os.path.exists(audio_output_folder):
        os.makedirs(audio_output_folder)

    file_list = list_files(
        video_input_folder, video_format
    )  # list_file innately has nat sorting
    grouped_files = {}

    for file in file_list:
        participant_id = os.path.basename(file)[:7]  # Using first 7 as "Participant ID", change for external IDs
        if participant_id not in grouped_files:
            grouped_files[participant_id] = []
        grouped_files[participant_id].append(file)

    for participant_id, files in tqdm(
        grouped_files.items(), desc="Processing Participant Files"
    ):
        files.sort()  # Ensure the files are in the correct order if not already
        output_filename = f"{participant_id}_concatenated.{audio_format}"  # Switch to _speech_language if needed
        output_path = os.path.join(audio_output_folder, output_filename)
        process_and_concatenate_videos(files, output_path, target_sample_rate)


__main__()
