"""This module provides utility functions for video and audio preprocessing."""
import argparse
import json
import os
import re
import tempfile
from typing import List, Tuple

import ffmpeg
import numpy as np
import pyloudnorm as pyln
import torch
import torchaudio


def extract_audio_from_video(video_path: str) -> bytes:
    """Extracts audio from video with no compression and returns audio bytes."""
    stream = ffmpeg.input(video_path)
    mixed_audio = ffmpeg.filter([stream], "amix", inputs=2, duration="longest")
    audio = mixed_audio.output("pipe:", format="wav", acodec="pcm_s16le")
    try:
        out, _ = ffmpeg.run(audio, capture_stdout=True, capture_stderr=True)
    except ffmpeg.Error as e:
        print("ffmpeg error:", e.stderr.decode("utf-8"))
        raise e
    return out


def convert_stereo_to_mono(waveform: torch.Tensor) -> torch.Tensor:
    """Checks and converts stereo audio waveform to mono by averaging the channels."""
    if waveform.shape[0] > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)
    return waveform


def resample_audio(waveform: torch.Tensor, orig_sample_rate: int, new_sample_rate: int = 16000) -> Tuple[torch.Tensor, int]:
    """Resamples the audio waveform to a new sample rate."""
    resampler = torchaudio.transforms.Resample(orig_freq=orig_sample_rate, new_freq=new_sample_rate)
    waveform_resampled = resampler(waveform)
    return waveform_resampled, new_sample_rate


def save_audio(waveform: torch.Tensor, sample_rate: int, output_path: str) -> None:
    """Saves the audio waveform to a WAV file with 16 bits per sample."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    torchaudio.save(output_path, waveform, sample_rate, bits_per_sample=16)


def load_audio_from_bytes(audio_bytes: bytes, format: str) -> Tuple[torch.Tensor, int]:
    """Loads audio from bytes by first writing to a temporary file, then loading it."""
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_bytes)
        temp_audio_file.seek(0)  # Go back to the start of the file
        waveform, sample_rate = torchaudio.load(temp_audio_file.name, format=format)
    return waveform, sample_rate


def normalize_loudness(audio: np.ndarray, rate: int, target_loudness: int = -23) -> torch.Tensor:
    """Normalizes the loudness of the audio to target_loudness."""
    meter = pyln.Meter(rate)  # create a BS.1770 meter
    current_loudness = meter.integrated_loudness(audio.squeeze())
    # Normalize the loudness of the audio to the target loudness level
    loudness_normalized_audio = pyln.normalize.loudness(audio.squeeze(), current_loudness, target_loudness)
    return torch.tensor(loudness_normalized_audio).unsqueeze(0)


def natural_sort_key(s: str) -> list:
    """Obtain a tuple that represents the natural order sort key of the input string."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def list_files(folder_path: str, format: str) -> List[str]:
    """List files in a nested folder structure with a specific format.
    
    Args:
        folder_path (str): The path to the folder.
        format (str): The file format to filter by, e.g., 'MXF'.
    
    Returns:
        List[str]: A list of file paths, sorted naturally.
    """
    # Modified to accommodate nested directory structures by participant ID
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith('.' + format):
                files.append(os.path.join(root, filename))
    files.sort(key=natural_sort_key)
    return files


def get_device() -> str:
    """Get the device (CPU or CUDA) for computation.

    Returns:
        str: The device string.

    """
    return "cuda" if torch.cuda.is_available() else "cpu"


def save_json(file: str, results: dict) -> None:
    """Saves the results as JSON."""
    with open(file, "w") as f:
        json.dump(results, f)


def process_and_concatenate_videos(video_files: List[str], output_path: str, target_sample_rate: int = 16000) -> None:
    """Processes and concatenates videos into a single audio waveform.

    Args:
        video_files (List[str]): A list of video file paths.
        output_path (str): The output path for the concatenated audio waveform.
        target_sample_rate (int, optional): The target sample rate default = 16000.

    Returns:
        None

    """
    concatenated_waveform = []
    for video_file in video_files:
        try:
            audio_bytes = extract_audio_from_video(video_file)
        except ffmpeg.Error:
            print(f"Error processing {video_file}, skipping.")
            continue

        waveform, sample_rate = load_audio_from_bytes(audio_bytes, "wav")
        waveform_mono = convert_stereo_to_mono(waveform)
        if sample_rate != target_sample_rate:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
            waveform = resampler(waveform_mono)
        concatenated_waveform.append(waveform)

    if concatenated_waveform:
        concatenated_waveform = torch.cat(concatenated_waveform, dim=1)
        save_audio(concatenated_waveform, target_sample_rate, output_path)


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments for Video and Audio Preprocessing."""
    parser = argparse.ArgumentParser(description="Video and Audio Preprocessing")
    parser.add_argument(
        "--video_folder",
        type=str,
        default="./data/videos",
        help="Path to the video folder"
    )
    parser.add_argument(
        "--audio_folder",
        type=str,
        default="./data/audios",
        help="Path to the audio folder"
    )
    parser.add_argument(
        "--participant_file",
        type=str,
        default=None,
        help="Path to the JSON file with participant IDs to process"
    )
    parser.add_argument(
        "--error_log",
        type=str,
        default="./error_log.json",
        help="Path to the error log file"
    )
    return parser.parse_args()
