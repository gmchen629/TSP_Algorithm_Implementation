import random
import sys
import os

from local_search import LocalSearch
from approx import nearest_neighbor
from branch_and_bound import BranchAndBound

def read_file(filename):
    '''
    This function reads *.tsp files and stores results in a dictionary called position.
    '''
    position = {} # key: locationID, value: [x coordinate, y coordinate]
    f = open(filename)
    lines = f.readlines()
    for line in lines:
        fields = line.split(" ")
        if (len(fields) < 3 or not fields[0].isdigit()):
            continue
        cityId = int(fields[0])
        x = float(fields[1])
        y = float(fields[2])
        position[cityId] = [x, y]
    f.close()
    return position

def write_trace(trace, filename):
    '''
    This function writes the trace.
    '''
    f = open(filename, 'w')
    for i in range(len(trace)):
        f.write(str(trace[i][0]))
        f.write(", ")
        f.write(str(int(trace[i][1])))
        f.write("\n")
    f.close()

def write_solution(cost, solution, filename):
    '''
    This function writes the solution.
    '''
    f = open(filename, 'w')
    f.write(str(int(cost)))
    f.write("\n")
    for i in range(len(solution)):
        f.write(str(solution[i]))
        if i < len(solution) - 1:
            f.write(",")
    f.close()

def get_output_filename(filename):
    '''
    This function turns a filepath into the corresponding city name.
    '''
    cities = ['Atlanta', 'Berlin', 'Boston', 'Champaign', 'Cincinnati', 'Denver', 'NYC', 'Philadelphia', 'Roanoke', 'SanFrancisco', 'Toronto', 'UKansasState', 'UMissouri']
    city = ' '
    for name in cities:
        if name in filename:
            city = name
            break
    traceFilename = city + "_" + algorithm + "_" + str(cutoff)
    solutionFilename = city + "_" + algorithm + "_" + str(cutoff)
    if (seed != -1):
        traceFilename += "_" + str(seed)
        solutionFilename += "_" + str(seed)
    return traceFilename, solutionFilename

if __name__ == "__main__":
    # parse command line arguments
    args = sys.argv[1:]
    if len(args) % 2 == 1:
        print("Invalid number of arguments.\n")
        exit()
    argMap = {}
    for i in range(len(args)):
        if i % 2 == 0:
            argMap[args[i]] = args[i + 1]

    filename = ""
    algorithm = ""
    cutoff = 0
    seed = -1
    for name in argMap.keys():
        value = argMap[name]
        if name == '-inst':
            filename = value
        if name == '-time':
            cutoff = int(value)
        if name == '-alg':
            algorithm = value
        if name == '-seed':
            seed = int(value)
    if seed >= 0:
        random.seed(seed)
    # parse input file into position dict
    position = read_file(filename)
    # call the corresponding algorithm module
    trace = []
    bestCost = 0.0
    bestSolution = []
    if algorithm == "Approx":
        bestCost, bestSolution, trace = nearest_neighbor(position, cutoff)
    elif algorithm == "LS1":
        ls = LocalSearch(position, cutoff, 1)
        ls.main()
        trace = ls.trace
        bestSolution = ls.transformSol
        bestCost = ls.bestCost
    elif algorithm == "LS2":
        ls = LocalSearch(position, cutoff, 2)
        ls.main()
        trace = ls.trace
        bestSolution = ls.transformSol
        bestCost = ls.bestCost
    elif algorithm == "BnB":
        bnbInput = []
        for nodeID, positions in position.items():
            curList = []
            curList.append(nodeID)
            curList.append(positions[0])
            curList.append(positions[1])
            bnbInput.append(curList)
        bnb = BranchAndBound(bnbInput, cutoff)
        bnb.main()
        trace = bnb.trace
        bestSolution = bnb.bestSolution
        bestCost = bnb.min_cost
        print(bestCost)
    # write outputs
    if not os.path.exists("output/"):
        os.makedirs("output/")
    traceFilename, solutionFilename = get_output_filename(filename)
    write_trace(trace, "output/" + traceFilename + ".trace")
    write_solution(bestCost, bestSolution, "output/" + solutionFilename + ".sol")
    
