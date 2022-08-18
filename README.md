# Dependency
To run our project, please have numpy 1.21.4 installed.


# File Structure
```
.
├── README.md
├── approx.py
├── branch_and_bound.py
├── local_search.py
├── tsp_main.py
└── data
    ├── Atlanta.tsp
    ├── Berlin.tsp
    ├── Boston.tsp
    ├── Champaign.tsp
    ├── Cincinnati.tsp
    ├── Denver.tsp
    ├── NYC.tsp
    ├── Philadelphia.tsp
    ├── Roanoke.tsp
    ├── SanFrancisco.tsp
    ├── Toronto.tsp
    ├── UKansasState.tsp
    ├── UMissouri.tsp
    └── solutions.csv
```

## Code Files
1. tsp_main.py
    - Parse command line arguments to perform corresponding algorithm on certain dataset with given cutoff time and random seed.
    - Read data files and store locations of each node.
    - Call corresponding algorithm module and get the solution and trace.
    - Write solution and trace to output files.
2. algorithm modules
    - approx.py: approximation heuristic (nearest neighbor)
    - branch_and_bound.py: branch and bound
    - local_search.py: local search (hill climbing and simulated annealing)

## Data Files
Each file ends with `.tsp` contains all locations in a city. `solutions.csv` contains the correct answer of each instance.

# How To Run
Please use the command line below to run our project.
```shell
python3 tsp_main.py -inst <cityname>  -time <cutoff_in_seconds> -alg [BnB | Approx | LS1 | LS2] [-seed <random_seed>]
```
- -alg: The algorithm to use. Please choose from `BnB` (branch and bound), `Approx` (approximation heuristic), `LS1` (hill climbing), `LS2` (simulated annealing).
- -inst: The filepath of a single input instance.
- -time: The cutoff time in seconds. The program will exit after the given time.
- -seed: The random seed for local search algorithms.

Example: The command below runs hill climbing for Atlanta for 600 seconds on random seed 1.
```shell
python3 tsp_main.py -inst data/Atlanta.tsp  -time 600 -alg LS1 -seed 1
```

# Output Files
Each run of the program generates 2 output files.
## Solution File
- file name: `<instance>_<method>_<cutoff>[_<random_seed>].sol`, e.g. Atlanta_BnB_600.sol or Cincinnati_LS1_600_4.sol.
- file format: 
    - Line 1: The total cost of the best solution found.
    - Line 2: List of 0-indexed vertex IDs of the TSP tour.
- file path: all files will be put in `output` folder.
## Trace File
- file name: `<instance>_<method>_<cutoff>[_<random_seed>].trace`, e.g. Atlanta_BnB_600.trace or Cincinnati_LS1_600_4.trace.
- file format: Each line has 2 comma-separated values. The first is the timestamp, the second is the cost of the best solution found till that time point.
- file path: all files will be put in `output` folder.