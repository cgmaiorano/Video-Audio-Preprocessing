import os
import json
from preprocess_utilities import list_files, parse_arguments, process_and_concatenate_videos
from tqdm import tqdm

def main() -> None:
    """This is the main function responsible for video and audio preprocessing."""
    args = parse_arguments()
    video_input_folder = args.video_folder
    audio_output_folder = args.audio_folder
    participant_file = args.participant_file
    error_log_path = args.error_log

    if not os.path.exists(audio_output_folder):
        os.makedirs(audio_output_folder)

    if not os.path.exists(os.path.dirname(error_log_path)):
        os.makedirs(os.path.dirname(error_log_path))

    failed_participants = []

    video_format = "MXF"
    file_list = list_files(video_input_folder, video_format)
    grouped_files = {}

    if participant_file:
        with open(participant_file, "r") as f:
            participant_ids = json.load(f)

        # Group files by participant ID extracted from directory names
        for file in file_list:
            participant_id = os.path.basename(os.path.dirname(file))
            if participant_id in participant_ids:
                if participant_id not in grouped_files:
                    grouped_files[participant_id] = []
                grouped_files[participant_id].append(file)
    else:
        for file in file_list:
            participant_id = os.path.basename(os.path.dirname(file))
            if participant_id not in grouped_files:
                grouped_files[participant_id] = []
            grouped_files[participant_id].append(file)

    for participant_id, files in tqdm(grouped_files.items(), desc="Processing Participants"):
        files.sort()  # Further ensure files are sorted if needed
        output_filename = f"{participant_id}_concatenated.wav"
        output_path = os.path.join(audio_output_folder, output_filename)
        if os.path.exists(output_path):
            print(f"Skipping {participant_id} as {output_filename} already exists.")
            continue
        try:
            process_and_concatenate_videos(files, output_path, 16000)
        except Exception as e:
            print(f"Failed to process participant {participant_id}: {e}")
            failed_participants.append(participant_id)

    if failed_participants:
        with open(error_log_path, "w") as f:
            json.dump(failed_participants, f)
        print(f"Failed participant IDs logged in {error_log_path}")

if __name__ == "__main__":
    main()
