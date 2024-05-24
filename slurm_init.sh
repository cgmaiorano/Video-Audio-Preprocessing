#!/bin/bash

#SBATCH --job-name=mobi_video_preproc
#SBATCH --output=mobi_video_preproc.out
#SBATCH -N1 --ntasks-per-node=1
#SBATCH --mem=40G

# Define variables for paths
CONDA_DIR="/home/$USER/miniconda"
CONDA_SH="$CONDA_DIR/etc/profile.d/conda.sh"
CONDA_ENV_NAME="video_preprocessing"
CONDA_ENV_DIR="$CONDA_DIR/envs/$CONDA_ENV_NAME"
FFMPEG_DIR="/home/$USER/ffmpeg"

# Install Miniconda if not already installed
if [ ! -d "$CONDA_DIR" ]; then
    echo "Installing Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /home/$USER/miniconda.sh
    bash /home/$USER/miniconda.sh -b -p $CONDA_DIR
    rm /home/$USER/miniconda.sh
fi

# Set up Conda path and initialize
export PATH="$CONDA_DIR/bin:$PATH"
source $CONDA_SH

# Create a new Conda environment if it doesn't exist
if [ ! -d "$CONDA_ENV_DIR" ]; then
    conda create --name $CONDA_ENV_NAME python=3.10 -y
fi

# Activate the environment
source activate $CONDA_ENV_NAME

# Clone the GitHub repository if not already cloned
if [ ! -d "/home/$USER/Video-Audio-Preprocessing" ]; then
    git clone --branch cleaning https://github.com/cgmaiorano/Video-Audio-Preprocessing.git /home/$USER/Video-Audio-Preprocessing
fi

# Navigate to the project directory
cd /home/$USER/Video-Audio-Preprocessing

# Install dependencies
pip install -r requirements.txt

# Install ffmpeg if not already installed
if [ ! -d "$FFMPEG_DIR" ]; then
    echo "Installing ffmpeg..."
    wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-static.tar.xz -O /home/$USER/ffmpeg-release-static.tar.xz
    mkdir -p $FFMPEG_DIR
    tar -xf /home/$USER/ffmpeg-release-static.tar.xz --strip-components=1 -C $FFMPEG_DIR
    rm /home/$USER/ffmpeg-release-static.tar.xz
fi

# Add ffmpeg to PATH
export PATH="$FFMPEG_DIR:$PATH"

# Execute the Python script with specified folders
python src/video_audio_preprocessing/main.py --video_folder /data2/hbn/ --audio_folder /home/$USER/Desktop/audio/

# Deactivate the environment at the end of the script
conda deactivate

