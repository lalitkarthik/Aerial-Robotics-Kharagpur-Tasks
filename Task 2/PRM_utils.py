import cv2
import numpy as np
from queue import PriorityQueue

#Roadmap base class
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



#Function to draw the circle
def draw_circle(image, coord):
    cv2.circle(image, coord, 2, (230,202,142), -1)


#Function for drawing the path
def draw_path(image, path):
    color = (119, 152, 168)
    thickness = 2

    for i in range(len(path) - 1):
        cv2.line(image, path[i], path[i + 1], color, thickness)


#Function to generate random points
def generate_random_points(coordinate1, lim_1, lim_2, n):
    for _ in range(n):
        point=tuple(int(np.random.uniform(x,y)) for x,y in [lim_1, lim_2])
        coordinate1.append(point)

#Function to calculate euclidean distance
def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

#function to find the close neighbours
def k_nearest_neighbours(points, point, k):
    distances=[]
    for p in points:
        distances.append((dist(point,p), p))
    distances.sort()
    return [p for _,p in distances[:k]] 

#Function to check if the line passes through the obstacle (Bresenhem's line drawing algo)
def obstacle_crossing(image, p1, p2, maze):
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
        
        if((x1,y1) in maze.obstacles):
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
