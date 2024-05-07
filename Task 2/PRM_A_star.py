import numpy as np
from queue import PriorityQueue

#Function to calculate euclidean distance
def dist(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5

#Path reconstruction for A-star
def reconstruct_path(node, camefrom):
    path=[]
    while node:
        path.append(node)
        node=camefrom.get(node)
    
    return path

#A-star algorithm for finding the path1
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