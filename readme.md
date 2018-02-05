# Pickaxe Config Assistant
Pickaxe Config Assistant (PCA) is a Python based script that can run [xmrig-nvidia](https://github.com/xmrig/xmrig-nvidia) or [xmrig-amd](https://github.com/xmrig/xmrig-amd) for a set period of time and then analyse what hashrate the configuration achieved. The configuration is handed into the application at runtime and then the number of threads/blocks in the config is iterated through until reaching the `threadsmax/intensitymax` and `blocksmax/worksizemax` values (Nvidia/AMD arguments).

After completing a run of XMRig using the current configuration, a JSON file is created containing the information about that run. Once all runs have been completed, a graph of the total results is created.

_Note, the `master` branch contains the most stable build available._


#### Table of contents
* [Features](#features)
* [Installation](#installation)
* [Usage Examples](#usage)
* [Donations](#donations)
* [Contact](#contact)


## Features
* Helps to identify the best thread and block values for any given Nvidia GPU that supports XMrig.
* PCA runs XMRig for a short time to analyse the output from XMRig's log.
* Generates a graph of the min, max, average and wattage draw from each thread/block settings.
* Generates JSON data for the information gathered.
* Fully automated benchmarking (rough).


## Progress
* ~~Basic graphing~~
* ~~XMRig Nvidia Support~~
* ~~XMRig AMD Support~~
* Simple data analysis saved as .json:
    * ~~Max Hashrate~~
    * ~~Min Hashrate~~
    * ~~Average Hashrate~~
    * ~~Average Wattage~~
    * Average Temperature
* ~~Windows support~~
* ~~Linux support~~
* Linux compatibility testing:
    * ~~Ubuntu~~
    * Other


## Installation
1. Have Python3+ installed, install the following package:
    * `pip install matplotlib`
2. Download the release version of [xmrig-nvidia](https://github.com/xmrig/xmrig-nvidia/releases) or [xmrig-amd](https://github.com/xmrig/xmrig-amd/releases) for your OS.
3. Clone this repository `git clone https://github.com/PentagonalCube/PickaxeConfigAssistant.git`.
4. Copy the `xmrig-nvidia`/`xmrig-amd` executable file from the XMRig release and paste it into the `PickaxeConfigAssistant/xmrig-nvidia/`/`PickaxeConfigAssistant/xmrig-amd/` folder.
    * On Linux you'll need to compile the XMRig source code before you can copy it, see their instructions on [compiling XMRig](https://github.com/xmrig/xmrig-nvidia/wiki/Ubuntu-Build)
5. Use Python3+ to run the `PickaxeConfigAssistant/main.py` file (`python3 main.py < **args >`) and hand in the arguments from the list below in order to configure it to your requirements.


## Usage - Nvidia
Default benchmark timing for a single setting [30x8] on a system with only 1 GPU (or GPU #0 is our target):
```
main.py --threads 30 --blocks 8
```

42 second benchmarks for the XMRig settings [28x8, 29x8, 30x8, 31x8, 32x8]:
```
main.py --index 0 --threads 28 --threadsmax 32 --threadsstep 1 --blocks 8 --blocksmax 8 --blocksstep 1 --affinity 0 --seconds 42
```

42 second benchmarks for the XMRig settings [28x9, 32x9, 28x10, 32x10] for a GPU at index 1 (GPU #1):
```
main.py --index 1 --threads 28 --threadsmax 32 --threadsstep 4 --blocks 9 --blocksmax 10 --blocksstep 1 --seconds 42
```

22 second benchmarks for XMRig settings with increasing threads for a GPU at index 3 (GPU #3):
```
main.py --index 3 --threads 8 --threadsmax 192 --threadsstep 8 --blocks 8 --seconds 22
```


## Usage - AMD
The usage is pretty the same as for Nvidia, but for AMD our threads/blocks become intensity/worksize.

Default benchmark timing for a single setting [256x8] on a system with only 1 GPU (or GPU #0 is our target):
```
main.py --intensity 256 --worksize 8
```

We can also use multiple threads for our workers when we have an AMD card [ 256x8, 256x8 ]:
```
main.py --intensity 256 --worksize 8 --workerthreads 2
```

The other values work in the same way, a 42 second benchmark for the XMRig settings [256x8, 512x8, 256x9, 512x9]
```
main.py --intensity 256 --worksize 8 --intensitymax 512 --worksizemax 9 --intensitystep 256 --worksizestep 1
```

### Command line options
```
  --mode            The mode we will run the analysis in (`--mode nvidia` or `--mode amd`)
  --seconds         The length of time in seconds we will run XMRig for (default: 42)

  --affinity        The CPU core that we should tie our GPU worker to (default: 0)
  --bsleep          The value for bsleep in our GPU worker (default: 25)
  --bfactor         The value for bfactor in our GPU worker (default: 12)

Nvidia:
  --threads         The number of threads to have in our GPU worker (default: 8)
  --blocks          The number of blocks to have in our GPU worker (default: 1)

  --threadsmax      Maximum number of threads for our GPU worker
  --threadsmin      Minimum number of threads for our GPU worker
  --threadsstep     The value we should increment our thread count by with each iteration (default: 1)

  --blocksmax       Maximum number of blocks for our GPU worker
  --blocksmin       Minimum number of blocks for our GPU worker
  --blocksstep      The value we should increment our block count by with each iteration (default: 1)
  
AMD:
  --intensity       The number of intensity to have in our GPU worker (default: 64)
  --worksize        The size of a work block for our GPU worker (default: 4)

  --intensitymax    Maximum intensity for our GPU worker
  --intensitymin    Minimum intensity for our GPU worker
  --intensitystep   The value we should increment our intensity by with each iteration (default: 1)

  --worksizemax     Maximum worksize for our GPU worker
  --worksizemin     Minimum worksize for our GPU worker
  --worksizestep    The value we should increment our worksize by with each iteration (default: 1)

  --workerthreads   The number of worker threads to run on this GPU (clones current configuration into _n_ threads), (default: 1)
```


## Donations
This software is provided free of charge with no advertisement of any kind, please consider donating if this is a project you would like to see improve faster than it normally would.
* XMR: 44tS9Hxcadqg8g4Vy8Tfxt7s41ktiXe2dHetBmuDA3UtX9bWhx6bHbw5E6XnkB69mZfk1GEzb6TVLX68CgirCcebFpVDRoX


## Contact
* mun@kerbin.xyz