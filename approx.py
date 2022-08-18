import time
import math

def nearest_neighbor(all_points, cut_off):
    values = all_points.values()

    points_list = list(values)
    start_time = time.time()

    size = len(points_list)
    min_distance = float('inf')
    trace = [] # record each path and the time takes to find it

    # going through each point as a starting point
    for point in range(size):
    
    
        start = point
        curr = start
        visited = [curr] # keep track of points in the tour
        distance = 0 # distance in each path
        nearest = float('inf') # use to keep track of smallest distance to next point (nearest neighbor)
        d = 0 # current distance to next point
        next_point = -1 # index of nearest neighbor
        
        while len(visited) < size: # going through each point as next point
            nearest = float('inf') #reset the smallest distance for a new point
            for i in range(size): # compare distance with all neighbors
                if i in visited: # skip if in the tour
                    continue
                d = round(math.sqrt((points_list[i][0]-points_list[curr][0])**2+(points_list[i][1]-points_list[curr][1])**2))

                if d < nearest:
                    nearest = d
                    next_point = i # update if closer than previous nearest neighbor

            distance = distance + nearest # update the path distance
            
            visited.append(next_point)
            curr = next_point # change the current point to nearest neighbor

        #add the last path to the start point
        d = round(math.sqrt((points_list[start][0]-points_list[curr][0])**2+(points_list[start][1]-points_list[curr][1])**2))
        distance = distance + d

        if distance < min_distance:
            min_distance = distance # update smallest path with different starting point
            best_path = visited
            trace.append([round(time.time() - start_time, 2), min_distance])

            if(time.time() - start_time > cut_off):
                return min_distance, best_path, trace
 
    return min_distance, best_path, trace