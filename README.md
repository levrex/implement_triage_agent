# Implement triage agent

## Download
You can download the files manually via this website or in terminal (if you have git):
```sh 
 git clone https://github.com/levrex/implement_triage_agent
```

## Installation

For Dutch readers that would like to implement our AI workflow (from RZWN) we have made a seperate User [instruction manual in Dutch](https://github.com/levrex/implement_triage_agent/blob/main/20250428_Gebruikshandleiding_SelectieHulp_tool_SlimmeTriage.pdf)

#### Windows systems:
Prerequisite: Install [Anaconda](https://www.anaconda.com/docs/getting-started/miniconda/main/) with Python version 3.6.13 This additionally installs the Anaconda Prompt, which you can find in the windows search bar. Use this Anaconda prompt to run the commands mentioned below. Or call conda from the command prompt directly.

### Importing required modules
Before running, please install the dependencies. (It is advised to first set up a conda environment).

#### Option 1: create custom kernel with conda (Bash or batch script)
prerequisite: conda3

```sh
$ bash build_conda_env.sh
```
  
or   
```cmd
$ build_conda_env.bat
```

#### Option 2: pip
prerequisite: pip

```sh
$ pip install -r requirements.txt
```

## How to use
Start a session in the windows terminal 

How to use: 

### Step 1. Activate conda environment (to ensure correct versions of modules, see build_conda_env.sh)
    ```sh
    conda activate triage_env
    ```
    
    
### Step 2. Run script & supply content as flag in string format (only after activating environment)
    ```sh
    python run_triage_agent.py --input 'Deze patient heeft reumatoide artritis, acpa positief , ochtend stijfheid sinds kindsaf, nu in remissie'
    ```
#### example output (JSON)
```sh
{
  "FMS": 0.08652999997138977,
  "RA": 0.20974136888980865,
  "OA": 0.19083213806152344,
  "Chronic": 0.45154139399528503
}
```



## Contact
If you experience difficulties with implementing the pipeline or if you have any other questions feel free to send me an e-mail. You can contact me on: t.d.maarseveen@lumc.nl 
