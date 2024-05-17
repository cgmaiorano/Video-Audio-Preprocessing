#!/bin/bash

#SBATCH --job-name=mobi_video_preproc
#SBATCH --output=mobi_video_preproc.out
#SBATCH -N1 --ntasks-per-node=4
#SBATCH --mem-per-cpu=10G

# Load Conda from your local installation
source /home/ikim/miniconda3/etc/profile.d/conda.sh

# Load FFMPEG from your local installation
export PATH=/home/ikim/ffmpeg/bin:$PATH

# Navigate to the project directory
cd /home/ikim/Video-Audio-Preprocessing

# Create a new Conda environment if it does not exist
srun bash -c 'if [ ! -d "/home/ikim/miniconda3/envs/video_preprocessing" ]; then conda create --prefix /home/ikim/miniconda3/envs/video_preprocessing python=3.10 -y; fi'

# Activate the environment
source activate /home/ikim/miniconda3/envs/video_preprocessing

# Install dependencies if not already installed
srun bash -c 'if [ ! -f "/home/ikim/miniconda3/envs/video_preprocessing/requirements_installed" ]; then pip install -r requirements.txt; touch /home/ikim/miniconda3/envs/video_preprocessing/requirements_installed; fi'

# Execute the Python script with specified folders
srun python src/video_audio_preprocessing/main.py --video_folder /home/ikim/Desktop/video_process --audio_folder /home/ikim/Desktop/audio/

# Deactivate the environment at the end of the script
conda deactivate
