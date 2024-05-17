#!/bin/bash

#SBATCH --job-name=mobi_video_preproc
#SBATCH --output=mobi_video_preproc.out
#SBATCH -N1 --ntasks-per-node=4
#SBATCH --mem-per-cpu=10G

# Define variables for paths
CONDA_DIR="/home/$USER/miniconda"
CONDA_SH="$CONDA_DIR/etc/profile.d/conda.sh"
CONDA_ENV_DIR="/home/$USER/.conda/envs/video_preprocessing"

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

# Ensure Conda uses local directories
echo -e "pkgs_dirs:\n  - /home/$USER/.conda/pkgs\nenvs_dirs:\n  - /home/$USER/.conda/envs" > /home/$USER/.condarc

# Create a new Conda environment if it doesn't exist
if [ ! -d "$CONDA_ENV_DIR" ]; then
    conda create --prefix $CONDA_ENV_DIR python=3.10 -y
fi

# Activate the environment
conda activate $CONDA_ENV_DIR

# Navigate to the project directory
cd /home/$USER/Video-Audio-Preprocessing

# Install dependencies
pip install -r requirements.txt

# Execute the Python script with specified folders
python src/video_audio_preprocessing/main.py --video_folder /data2/hbn/ --audio_folder /home/$USER/Desktop/audio/

# Deactivate the environment at the end of the script
conda deactivate
