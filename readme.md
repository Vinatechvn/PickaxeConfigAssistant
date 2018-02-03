# Pickaxe Config Assistant
Pickaxe Config Assistant (PCA) is a Python based script that can run [xmrig-nvidia](https://github.com/xmrig/xmrig-nvidia) for a set period of time and then analyse what hashrate the configuration achieved. The configuration is handed into the application at runtime and then the number of threads/blocks in the config is iterated through until reaching the `threadsmax` and `blocksmax` values.

After completing a run of XMRig using the current configuration, a JSON file is created containing the information about that run. Once all runs have been completed, a graph of the total results is created.

_Please note only Windows support is available right now, the Python script should be compatible with Linux but this is work planned for the near future._


#### Table of contents
* [Features](#features)
* [Usage](#usage)
* [Donations](#donations)
* [Contact](#contact)


## Features
* Helps to identify the best thread and block values for any given Nvidia GPU that supports XMrig.
* PCA runs XMRig for a short time to analyse the output from XMRig's log.
* Generates a graph of the min, max, average and wattage draw from each thread/block settings.
* Generates JSON data for the information gathered.
* Fully automated benchmarking (rough).


## Usage
1. Download the release version of [xmrig-nvidia](https://github.com/xmrig/xmrig-nvidia/releases).
2. Download this repository.
3. Copy the `xmrig-nvidia.exe` file into the `xmrig-nvidia` folder of the downloaded copy of Pickaxe Config Assistant.
4. Use Python3+ to run the `main.py` file and hand in the arguments from the list below in order to configure it to your requirements.

### Command line options
```
  --seconds			The length of time in seconds we will run XMRig for (default: 42)

  --threads 			The number of threads to have in our GPU worker (default: 8)
  --blocks			The number of blocks to have in our GPU worker (default: 1)

  --threadsmax			Maximum number of threads for our GPU worker
  --threadsmin			Minimum number of threads for our GPU worker
  --threadsstep			The steps we should increment our thread count with each iteration (default: 1)

  --blocksmax			Maximum number of blocks for our GPU worker
  --blocksmin			Minimum number of blocks for our GPU worker
  --blocksstep			The steps we should increment our block count with each iteration (default: 1)

  --affinity			The CPU core that we should tie our GPU worker to (default: 0)
  --bsleep			The value for bsleep in our GPU worker (default: 25)
  --bfactor			The value for bfactor in our GPU worker (default: 12)
```

### Usage Examples
The command below will run a 42 second benchmark for the XMRig settings [28x8, 29x8, 30x8, 31x8, 32x8].
```
main.py --index 0 --threads 28 --threadsmax 32 --threadsstep 1 --blocks 8 --blocksmax 8 --blocksstep 1 --affinity 1 --seconds 42 
```


## Donations
This software is provided free of charge with no advertisment of any kind, please consider donating if this is a project you would like to see improve faster than it normally would.
* XMR: 44tS9Hxcadqg8g4Vy8Tfxt7s41ktiXe2dHetBmuDA3UtX9bWhx6bHbw5E6XnkB69mZfk1GEzb6TVLX68CgirCcebFpVDRoX


## Contact
* mun@kerbin.xyz