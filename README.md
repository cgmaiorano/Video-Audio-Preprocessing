# HBN Video and Audio Preprocessing
this repository extracts audio from video recordings, concatenates multiple segments of the same participant session, and resamples the waveform to the selected sample rate

## Requirements: ffmpeg
this repository requires native download of ffmpeg from the developer site: https://ffmpeg.org/download.html

## Requirements: python 3.9 
``` 
conda create -n preprocess-env python=3.9
```

## Installation:
```
pip install -r requirements.txt
```

## Quick start:
```
python main.py
```
