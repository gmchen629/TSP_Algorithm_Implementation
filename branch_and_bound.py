import time
import math

class BranchAndBound:
    def __init__(self,input_data,cutoff):
        self.input = input_data         # input data
        self.nodeNum = len(input_data)  # node number
        self.cutoff = cutoff            # cutoff time
        self.distances = []             # distance lists
        self.trace = []                 # output trace
        self.min_cost = float("inf")    # initialzed cost
        self.bestSolution = []          # final solution
        self.timestamp = 0              # timestamp to decide when we stop
        self.costMap = {}               #  a map to find the cost of each node
        self.nodePath = {}              # a map to find the visited path of current node
        self.isVisited = {}             # a map to  check if some has been visited by the current node

    #define a city class to start the graph
    class Position:
        def __init__(self,id):
            self.dumNode = id

    def calculateDistance(self,input): # calculate the distance and save the edges in ascending order for MST
        for i in range(self.nodeNum):
            temp_list = []      # initialize temp list to save the distances between other nodes and current node
            for j in range(self.nodeNum):
                distance = float("inf")  # if i == j, distance is inf
                if i != j:
                    distance = math.sqrt((input[i][1] - input[j][1]) ** 2 + (input[i][2] - input[j][2]) ** 2) #calculate the distance between 2 nodes
                temp_list.append(distance) # save the distances between other nodes and current node
            self.distances.append(temp_list)      # save the distances between other nodes and current node
        return self.distances

    def findBound(self,node,nodeNum):
        lower_bound = self.costMap[node]  # find the current bound
        first_bound = float("inf")
        second_bound = float("inf")
        for i in range(nodeNum):
            if self.isVisited[node][i] != True:     # if find the next node that is not visited by the current node
                for first in range(nodeNum):
                    if (self.distances[i][first]< first_bound):
                        first_bound = self.distances[i][first]    # calculate the first bound
                for second in range(nodeNum):
                    if (self.distances[i][second]< second_bound):
                        second_bound = self.distances[i][second]  # calculate the second bound
                lower_bound += (first_bound + second_bound) / 2         # calculate the lower_bound
        return lower_bound

    def BnB(self,beginning,costMap,nodePath):
        # initialize a node to start the loop
        start = self.Position(0)
        nodePath[start] = [beginning]
        costMap[start] = 0
        self.isVisited[start] = [False] * self.nodeNum
        self.isVisited[start][0] = True
        # initialize the stack
        stack = []
        stack.append(start)
        # start the loop until the stack is empty
        while len(stack) > 0:
            if time.time() - self.timestamp> self.cutoff: # stop if out of time
                return
            current = stack[-1]   # find the current node
            stack = stack[0:-1]    # update the stack
            # check if the cost of current node is less than the mini cost
            if self.min_cost <= costMap[current]:
                continue
            # if last node, calculate the new cost
            if len(nodePath[current]) == self.nodeNum:
                new_cost = costMap[current] + self.distances[nodePath[current][-1]][nodePath[current][0]]
                if new_cost < self.min_cost:
                    self.min_cost = new_cost
                    self.bestSolution = list(nodePath[current])
                    self.trace.append([round(time.time() - self.timestamp, 2), self.min_cost])
            else:
                for i in range(self.nodeNum):
                    if i not in nodePath[current]:  # check if node is not visited by the current path
                        new_cost = costMap[current] + self.distances[nodePath[current][-1]][i]
                        # if new cost is less than the quality, add node to stack
                        if new_cost < self.min_cost:
                            next_node = self.Position(0)
                            self.isVisited[next_node] = self.isVisited[current].copy()
                            self.isVisited[next_node][i] = True
                            new_path = nodePath[current].copy()
                            new_path.append(i)
                            nodePath[next_node] = new_path
                            costMap[next_node] = new_cost
                            lower_bound = self.findBound(next_node, self.nodeNum)
                            if lower_bound < self.min_cost:
                                stack.append(next_node)

    def main(self):
        self.calculateDistance(self.input) # calculate the distances
        self.timestamp = time.time() # start to count the time
        self.BnB(0, self.costMap, self.nodePath)  # calculate the solution