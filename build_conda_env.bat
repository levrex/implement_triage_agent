:: Dependencies: Anaconda or Miniconda installed

@echo off
REM Create a conda environment for machine learning
conda create -n triage_env python=3.6.13 -y

REM Activate the conda environment
call conda activate triage_env

REM Upgrade pip and install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Deactivate the environment
call conda deactivate

echo Environment 'triage_env' setup complete.
pause
