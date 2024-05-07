import cv2
import numpy as np
import math
from queue import PriorityQueue 

class RoadMap:
    def __init__(self):
        self.nodes=[]
        self.edges={}
        self.obstacles=[]

    def add_obstacles(self, coord):
        self.obstacles.append(coord)

    def add_nodes(self, coord):
        self.nodes.append(coord)

    def add_neighbours(self,node1, node2):
        if(node1 in self.edges):
            self.edges[node1].append(node2)
        else:
            self.edges[node1]=[node2]

def generate_random_points():
    coordinate=[]
    for _ in range(500):
        point=tuple(int(np.random.uniform(x,y)) for x,y in [(0,50), (0,50)])
        coordinate.append(point)
    return coordinate

def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

def k_nearest_neighbours(points, point, k):
    distances=[]
    for p in points:
        distances.append((dist(point,p), p))
    distances.sort()
    return [p for _,p in distances[:k]] 

#Function to check if the line passes through the obstacle
def obstacle_crossing(image, p1, p2, obstacles):
    x1, y1 = p1
    x2, y2 = p2

    dx = abs(x2 - x1)
    dy = -abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    err = dx + dy

    while True:
        if x1 == x2 and y1 == y2:
            break
        
        if((x1,y1) in obstacles):
            return True

        e2 = 2 * err
        if e2 >= dy:
            if x1 == x2:
                break
            err += dy
            x1 += sx
        if e2 <= dx:
            if y1 == y2:
                break
            err += dx
            y1 += sy

    return False


def reconstruct_path(node, camefrom):
    path=[]
    while node:
        path.append(node)
        node=camefrom.get(node)
    
    return path

def astar(graph, start, goal):
    count=0
    open_set=PriorityQueue()
    closed_set=[]
    camefrom={}
    g_score={node: float('inf') for node in graph.nodes}
    f_score={node: float('inf') for node in graph.nodes}
    g_score[start]=0
    f_score[start]=dist(start, goal)

    open_set.put((f_score[start], count, start))

    open_set_hash={start}

    while not open_set.empty():

        current_node=open_set.get()[2]

        if(current_node==goal):
            camefrom[goal]=prev_node
            return reconstruct_path(goal, camefrom)
        
        open_set_hash.remove(current_node)
        closed_set.append(current_node)
        prev_node=current_node

        for neighbor in graph.edges.get(current_node, []):
            if neighbor in closed_set:
                continue
            
            tentative_g_score = g_score[current_node] + dist(current_node, neighbor)
            
            if tentative_g_score<g_score[neighbor]:
                camefrom[neighbor]=current_node
                g_score[neighbor]=tentative_g_score
                f_score[neighbor]=g_score[neighbor]+dist(neighbor, goal)
            else:
                continue

            if neighbor not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        
    
    return None


