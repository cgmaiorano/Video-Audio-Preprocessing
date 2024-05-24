#!/bin/bash

#SBATCH --job-name=mobi_video_preproc_part4
#SBATCH --output=mobi_video_preproc_part4.out
#SBATCH -N1 --ntasks-per-node=1
#SBATCH --mem=16G

# Define variables for paths
CONDA_DIR="/home/$USER/miniconda"
CONDA_SH="$CONDA_DIR/etc/profile.d/conda.sh"
CONDA_ENV_NAME="video_preprocessing"
FFMPEG_DIR="/home/$USER/ffmpeg"

# Set up Conda path and initialize
export PATH="$CONDA_DIR/bin:$PATH"
source $CONDA_SH

# Activate the environment
source activate $CONDA_ENV_NAME

# Add ffmpeg to PATH
export PATH="$FFMPEG_DIR:$PATH"

# Navigate to the project directory
cd /home/$USER/Video-Audio-Preprocessing

# Execute the Python script with specified folders
python src/video_audio_preprocessing/main.py --video_folder /data3/hbn/voice_data/website_uploads/MRI_Speech_Language --audio_folder /data3/mobi/hbn_video_qa/extracted_audio --participant_file participants_part_4.json --error_log error_log_part_4.json

# Deactivate the environment at the end of the script
conda deactivate
