import cv2
import numpy as np
import random
from queue import PriorityQueue
from PRM_A_star import astar
from PRM_utils import RoadMap, generate_random_points, draw_circle, draw_path, k_nearest_neighbours, obstacle_crossing
from PRM_Turtle import turtle


#Parameter definition (found using hit and trial after experimenting)
points_generated= 500
nearest_neighbours= 10


#Loading the image
img=cv2.imread("maze.png")

#Conversion to grayscale and binarizing it
gray=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
_, binary= cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
mask= cv2.bitwise_not(binary)

img_copy= img.copy()

maze=RoadMap() #Initialising the roadmap for start easy


#Drawing the obstacles
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        if mask[y, x]==255:
            cv2.rectangle(img_copy, (x,y), (x+1, y+1), (83,86,91),1)

#Adding the obstacles to raodmap
for y in range(img.shape[0]): 
    for x in range(img.shape[1]):
        if np.any(img_copy[y, x] == [83,86,91]):  
            maze.add_obstacles((x,y))

img_copy_1=img_copy.copy()

#Generating Random points and drawing it
coordinate=[]
random.seed(42)
generate_random_points(coordinate, (8,450), (20, 335), points_generated)

#Initializing the start and end points
start1= (40,330)
end1=(100,330)

start2= (160,25)
end2=(445,300)

coordinate.append(start1)
coordinate.append(end1)
coordinate.append(start2)
coordinate.append(end2)

cv2.imshow("Maze", img_copy_1)
cv2.waitKey(1000)
cv2.destroyAllWindows()

#Drawing the nodes 
for coord in coordinate:
    if(coord not in maze.obstacles):
        draw_circle(img_copy_1, coord)
        maze.add_nodes(coord)

line_copy=img_copy_1.copy()

for point in maze.nodes:
    neighbours=k_nearest_neighbours(maze.nodes, point, nearest_neighbours)
    for neighbour in neighbours:
        if point!=neighbour:
            if not obstacle_crossing(img_copy_1, point, neighbour, maze):
                maze.add_neighbours(point, neighbour)
                cv2.line(line_copy, point, neighbour, (168,149,136), 1)
                cv2.imshow("Line", line_copy)
                cv2.waitKey(1)

def first_part():
    path1=astar(maze, start1, end1)
    line_copy_1=line_copy.copy()
    img_copy_path_1=img_copy_1.copy()
    if path1:
        draw_path(line_copy_1, path1)  # Draw the path1 on the image
        draw_path(img_copy_path_1, path1)
    else:
        print("Path not found")

    cv2.imshow("Line with path1", line_copy_1)
    cv2.waitKey(1000)

    cv2.imshow("Path_1", img_copy_path_1)
    cv2.waitKey(2000)
    cv2.imwrite("Start_Easy.png", img_copy_path_1)
    cv2.destroyAllWindows()


def second_part():
    path2=astar(maze, start2, end2)
    line_copy_2=line_copy.copy()
    img_copy_path_2=img_copy_1.copy()
    if path2:
        draw_path(line_copy_2, path2)  # Draw the path2 on the image
        draw_path(img_copy_path_2, path2)
    else:
        print("Path not found")

    cv2.imshow("Line with path2", line_copy_2)
    cv2.waitKey(1000)

    cv2.imshow("Path_2", img_copy_path_2)
    cv2.waitKey(2000)
    cv2.imwrite("Start_Hard.png", img_copy_path_2)
    cv2.destroyAllWindows()


first_part()
second_part()
