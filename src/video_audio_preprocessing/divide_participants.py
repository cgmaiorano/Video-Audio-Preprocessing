"""This module provides functions for dividing participants."""
import json
import os
import re
from typing import List


def list_files(folder_path: str, format: str) -> List[str]:
    """List files in a nested folder structure with a specific format.
    
    Args:
        folder_path (str): The path to the folder.
        format (str): The file format to filter.

    Returns:
        List[str]: A list of file paths.
    """
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.' + format):
                files.append(os.path.join(root, filename))
    files.sort(key=natural_sort_key)
    return files

def natural_sort_key(s: str) -> list:
    """Obtain a tuple that represents the natural order sort key of the input string."""
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r'(\d+)', s)
    ]

video_input_folder = "/data3/hbn/voice_data/website_uploads/MRI_Speech_Language"
audio_output_folder = "/data3/mobi/hbn_video_qa/extracted_audio"
video_format = "MXF"

file_list = list_files(video_input_folder, video_format)
grouped_files = {}

for file in file_list:
    participant_id = os.path.basename(os.path.dirname(file))
    if participant_id not in grouped_files:
        grouped_files[participant_id] = []
    grouped_files[participant_id].append(file)

# Get list of all participant IDs
participant_ids = list(grouped_files.keys())

# Split the participant IDs into 4 parts
split_participants = [
    participant_ids[i::4] for i in range(4)
]

# Save split participants to JSON files
for i, split in enumerate(split_participants):
    with open(f"participants_part_{i+1}.json", "w") as f:
        json.dump(split, f)
