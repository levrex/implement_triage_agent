# Implement triage agent


## Installation


#### Windows systems:
Prerequisite: Install [Anaconda](https://www.anaconda.com/distribution/) with python version 3.6+. This additionally installs the Anaconda Prompt, which you can find in the windows search bar. Use this Anaconda prompt to run the commands mentioned below.

#### Linux / Windows (dev) systems:
Prerequisite: [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) environment (with jupyter notebook). Use the terminal to run the commands mentioned below.

Install Jupyter Notebook:
```sh
$ conda install -c anaconda notebook
```

### Importing required modules
Before running, please install the dependencies. 

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

### 1. Activate conda environment (to ensure correct versions of modules, see build_conda_env.sh)
    ```sh
    $ source activate triage_env
    ```
    
    
### 2. Run script & supply content as flag in string format
    ```sh
    $ python script.py --input 'Deze patient heeft reumatoide artritis, acpa positief , ochtend stijfheid sinds kindsaf, nu in remissie'
    ```
#### example output (JSON)
```sh{
  "FMS": 0.3859322667121887,
  "RA": 0.05707930028438568,
  "OA": 0.19083213806152344
}
```



## Contact
If you experience difficulties with implementing the pipeline or if you have any other questions feel free to send me an e-mail. You can contact me on: t.d.maarseveen@lumc.nl 
