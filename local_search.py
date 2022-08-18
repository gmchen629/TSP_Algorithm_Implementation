import random
import time
import math

def getDistance(position, city1, city2, distanceMap):
    '''
    This function returns the distance between city1 and city2.
    '''
    if tuple([city1, city2]) in distanceMap.keys():
        return distanceMap[tuple([city1, city2])]
    x1 = position[city1][0]
    x2 = position[city2][0]
    y1 = position[city1][1]
    y2 = position[city2][1]
    distance = math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))
    distanceMap[tuple([city1, city2])] = distance
    return distance

def getCost(solution, position, distanceMap):
    '''
    This function calculates the total cost on a given sequence of locations.
    '''
    cost = float(0.0)
    for i in range(len(solution) - 1):
        cost += getDistance(position, solution[i], solution[i + 1], distanceMap)
    cost += getDistance(position, solution[0], solution[-1], distanceMap)
    return cost

class LocalSearch:
    def __init__(self, position, cutOff, type):
        self.position = position        # the position of each node
        self.distanceMap = {}           # the memo map for distances bewteen each pair of nodes
        self.startTime = time.time()    # starting time of execution
        self.cutOff = cutOff            # cutoff time to end execution
        self.curCost = 0                # the total cost of the current solution
        self.curSolution = []           # the current solution
        self.bestCost = 0               # the total cost of the best solution
        self.bestSolution = []          # the best solution
        self.visited = set()            # all visited solutions
        self.trace = []                 # list of traces
        self.type = type                # 1: hill climbing, 2: simulated annealing
        self.p = 0.95                   # the probability to go to a worse neighbor in simulated annealing
        self.transformSol = []          # the 0-indexed solution
    
    def randomizeSolution(self, locationIDs):
        '''
        This function randomly shuffles nodes in the solution.
        '''
        random.shuffle(locationIDs)
        cost = getCost(locationIDs, self.position, self.distanceMap)
        self.curCost = cost
        self.curSolution = locationIDs[:]

    def getInitialSolution(self, locationIDs):
        '''
        This function returns the initial solution for local search.
        '''
        # get the initial solution by nearest neighbor approximation heurisitics
        solution = [1]
        tmpVisited = set() # visited nodes
        cur = locationIDs[0]
        tmpVisited.add(cur)
        while len(tmpVisited) < len(locationIDs):
            minDis = -1
            next = cur
            # among all unvisited nodes, find the one nearest to the current node
            for i in range(len(locationIDs)):
                candidate = locationIDs[i]
                if candidate in tmpVisited:
                    continue
                curDis = getDistance(self.position, cur, candidate, self.distanceMap)
                if minDis == -1 or minDis > curDis:
                    minDis = curDis
                    next = candidate
            solution.append(next)
            tmpVisited.add(next)
            cur = next
        # randomly shuffle 3 slices of the current solution
        start = int(0.2 * len(solution))
        end = int(0.3 * len(solution))
        solution[start:end] = sorted(solution[start:end], key=lambda x: random.random())
        start = int(0.5 * len(solution))
        end = int(0.6 * len(solution))
        solution[start:end] = sorted(solution[start:end], key=lambda x: random.random())
        start = int(0.8 * len(solution))
        end = int(0.9 * len(solution))
        solution[start:end] = sorted(solution[start:end], key=lambda x: random.random())
        # set the current and best solution to be the initial solution
        cost = getCost(solution, self.position, self.distanceMap)
        self.curCost = cost
        self.curSolution = solution[:]
        self.bestCost = cost
        self.bestSolution = solution[:]

    def localSearch1(self):
        '''
        This function performs hill climbing local search.
        '''
        cityNum = len(self.curSolution)
        chosenNeighbor = []
        chosenNeighborCost = 0.0
        largestImprove = 0.0
        # use 2-opt to generate the neighborhood
        for i in range(cityNum):
            for j in range(i + 1, cityNum):
                neighborSolution = self.curSolution[:]
                neighborSolution[i] = self.curSolution[j]
                neighborSolution[j] = self.curSolution[i]
                if tuple(neighborSolution) in self.visited:
                    # skip visited solution
                    continue
                chosenNeighborCost = getCost(neighborSolution, self.position, self.distanceMap)
                if self.curCost - chosenNeighborCost > largestImprove:
                    # choose the neighbor with largest improvement on total cost
                    largestImprove = self.curCost - chosenNeighborCost
                    chosenNeighbor = neighborSolution[:]
        if len(chosenNeighbor) == 0:
            # neighborhood is empty, tell the main function to restart local search with a random initial solution
            return True
        self.visited.add(tuple(chosenNeighbor))
        # set the chosen neighbor to be the current solution
        self.curSolution = chosenNeighbor[:]
        self.curCost = chosenNeighborCost
        if self.curCost < self.bestCost:
            # update the best solution and add a trace
            self.bestCost = self.curCost
            self.bestSolution = self.curSolution[:]
            curTrace = []
            curTrace.append(round(time.time() - self.startTime, 2))
            curTrace.append(self.bestCost)
            self.trace.append(curTrace)
        return False

    def localSearch2(self):
        '''
        This function performs simulated annealing local search.
        '''
        self.p *= 0.95 # the probability to move to a worse neighbor
        cityNum = len(self.curSolution)
        chosenNeighbor = []
        chosenNeighborCost = 0.0
        for i in range(int(cityNum * (cityNum - 1) / 2)):
            # use 2-opt to generate the neighborhood, randomly select one neighbor
            cityPair = random.sample(range(cityNum), 2)
            neighborSolution = self.curSolution[:]
            neighborSolution[cityPair[0]] = self.curSolution[cityPair[1]]
            neighborSolution[cityPair[1]] = self.curSolution[cityPair[0]]
            if tuple(neighborSolution) in self.visited:
                # skip visited solution
                continue
            chosenNeighbor = neighborSolution[:]
            chosenNeighborCost = getCost(neighborSolution, self.position, self.distanceMap)
            break
        if len(chosenNeighbor) == 0:
            # neighborhood is empty, tell the main function to restart local search with a random initial solution
            return True
        if chosenNeighborCost < self.curCost or random.random() <= self.p:
            # move to a better neighbor or a worse neighbor with probability p
            self.visited.add(tuple(chosenNeighbor))
            self.curSolution = chosenNeighbor[:]
            self.curCost = chosenNeighborCost
        if self.curCost < self.bestCost:
            # update the best solution and add a trace
            self.bestCost = self.curCost
            self.bestSolution = self.curSolution[:]
            curTrace = []
            curTrace.append(round(time.time() - self.startTime, 2))
            curTrace.append(self.bestCost)
            self.trace.append(curTrace)
        return False

    def transformSolution(self):
        '''
        This function transforms 1-indexed solution to 0-indexed solution.
        '''
        for i in range(len(self.bestSolution)):
            self.transformSol.append(self.bestSolution[i] - 1)

    def main(self):
        self.getInitialSolution(list(self.position.keys()))
        curTrace = []
        curTrace.append(round(time.time() - self.startTime, 2))
        curTrace.append(self.bestCost)
        self.trace.append(curTrace)
        self.visited.add(tuple(self.curSolution))
        while True:
            if (time.time() - self.startTime > self.cutOff):
                # ends execution when time is up
                break
            if self.type == 1:
                # perform hill climbing
                noNeighbor = self.localSearch1()
            else:
                # perform simulated annealing
                noNeighbor = self.localSearch2()
            if noNeighbor == True:
                # random restart
                self.randomizeSolution(self.curSolution)
        self.transformSolution()