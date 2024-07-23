# HBN Video and Audio Preprocessing
this repository extracts audio from video recordings, concatenates multiple segments of the same participant session, and resamples the waveform to the selected sample rate

## Requirements: ffmpeg
this repository requires native download of ffmpeg from the developer site: https://ffmpeg.org/download.html

## Installation:
```
conda env create -f environment.yml
poetry install
```

## Quick start:
```
python main.py
```
