from utils import Player, WINDOW_WIDTH
import cv2
import numpy as np
from PRM_localization import RoadMap, generate_random_points, k_nearest_neighbours, obstacle_crossing, dist, astar
from queue import PriorityQueue

player = Player()
# Initializing a Player object with a random start position on a randomly generated Maze


def strategy():
    # This function is to localize the position of the newly created player with respect to the 
    
    #This uses PRM to find the next position of the Drone
    def drone_next_pos(sub_maze):
        img_copy= sub_maze.copy()
        sub_part=RoadMap()
        
        drone_pos = (sub_maze.shape[1] // 2, sub_maze.shape[0] // 2)  

        for y in range(sub_maze.shape[0]):
            for x in range(sub_maze.shape[1]):
                if sub_maze[y, x] == 0:  
                    sub_part.add_obstacles((x, y))  

        coordinate=generate_random_points()
        coordinate.append(drone_pos)

        for coord in coordinate:
            if(coord not in sub_part.obstacles):
                sub_part.add_nodes(coord)

        for point in sub_part.nodes:
            neighbours=k_nearest_neighbours(sub_part.nodes, point, 10)
            for neighbour in neighbours:
                if point!=neighbour:
                    if not obstacle_crossing(img_copy, point, neighbour, sub_part.obstacles):
                        sub_part.add_neighbours(point, neighbour)
        
        distance=[]
        for point in sub_part.nodes:
            distance.append((dist(point, drone_pos), point))
        distance.sort(reverse=True)
        

        for _, point in distance:
            path= astar(sub_part, drone_pos, point)
            if (path and len(path)<=3):
                return path
        return []
        

    base=np.array(player.getMap()) #The reference map
    initial_snap=np.array(player.getSnapShot()) #Initial snapshot
    h,w=initial_snap.shape
    total_possibilities=0 #Captures the number of total possible initial matches

    #All the possible methods for template matching referred from open CV documentation
    methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]

    start_pos=[] #Array to store all the possible initial starting positions
    hierarchy=PriorityQueue() #For storing the initial different positions on the basis of difference

    #Processing based on OpenCV documentation
    for meth in methods:
        base_copy = base.copy()

        result = cv2.matchTemplate(base_copy, initial_snap, meth)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if meth in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0]+w, top_left[1]+h)

        if ((top_left,bottom_right)) not in start_pos:
            start_pos.append((top_left,bottom_right)) #Adds the possible start position to the arra

    #Calculates the next possible position
    next_pos_path=drone_next_pos(initial_snap)

    for coord in next_pos_path:
        player.move_vertical(coord[1] - initial_snap.shape[1]//2 )
        player.move_horizontal(coord[0] - initial_snap.shape[0]//2 )

    for ((s_t_l,s_b_r)) in start_pos:
        total_possibilities+=1
        base_copy = base.copy()
        drone_pos=((s_t_l[0] + h//2, s_t_l[1] + h//2))
        cv2.circle(base_copy, drone_pos, 3, (0,255,0), -1)
        cv2.rectangle(base_copy, s_t_l, s_b_r, (0,255,0), 2)
        cv2.imshow("Initial_match{total_possibilities}", base_copy)
        cv2.imshow("Initial_snap", initial_snap)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        for i in range(len(next_pos_path)-1):
            start_point = (s_t_l[0] + next_pos_path[i][0], s_t_l[1] + next_pos_path[i][1])
            end_point = (s_t_l[0] + next_pos_path[i+1][0], s_t_l[1] + next_pos_path[i+1][1])
            cv2.line(base_copy, start_point, end_point, (0, 255, 0), 2)
        cv2.imshow("Path visualisation for initial condition and match {total_possibilities}", base_copy)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 

    for i in range(1,6):
        snap=np.array(player.getSnapShot())
        pos=[]
        for meth in methods:
            base_copy = base.copy()

            result = cv2.matchTemplate(base_copy, snap, meth)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if meth in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc

            bottom_right = (top_left[0]+w, top_left[1]+h)

            if ((top_left,bottom_right)) not in pos:
                pos.append((top_left,bottom_right))

        next_pos_path=drone_next_pos(snap)

        for ((t_l,b_r)) in pos:
            base_copy = base.copy()
            drone_pos=((t_l[0] + h//2, t_l[1] + h//2))
            cv2.circle(base_copy, drone_pos, 3, (0,255,0), -1)
            cv2.rectangle(base_copy, t_l, b_r, (0,255,0), 2)
            cv2.imshow(f"Match {i}", base_copy)
            cv2.imshow(f"Snap {i}", snap)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            for j in range(len(next_pos_path)-1):
                start_point = (t_l[0] + next_pos_path[j][0], t_l[1] + next_pos_path[j][1])
                end_point = (t_l[0] + next_pos_path[j + 1][0], t_l[1] + next_pos_path[j + 1][1])
                cv2.line(base_copy, start_point, end_point, (0, 255, 0), 2)
            cv2.imshow(f"Path visualisation for {i}th condition", base_copy)
            cv2.waitKey(0)
            cv2.destroyAllWindows() 
            for ((s_t_l,s_b_r)) in start_pos:
                hierarchy.put((dist(s_t_l,t_l), (s_t_l,s_b_r)))  #Fills the priority queue based on the distance between various starting points and the current snapshot point
        
        for coord in next_pos_path:
            player.move_vertical(coord[1] - snap.shape[0]//2 )
            player.move_horizontal(coord[0] - snap.shape[1]//2 )

    (starting_tl, starting_br)= hierarchy.get()[1]
    drone_initial_position=(starting_tl[0] +w//2, starting_tl[1] +h//2)
    print(f"Drone's Initial Position is {drone_initial_position}")
    base_copy=base.copy()
    cv2.rectangle(base_copy, starting_tl, starting_br, (0,255,0), 2)
    cv2.circle(base_copy, drone_initial_position, 2, (0,255,0),-1)
    cv2.imshow("Finalised Initial Position", base_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    strategy()
    map = np.array(player.getMap())
    cv2.imwrite("map.png", map * 255)

    snap = np.array(player.getSnapShot())
    cv2.imwrite("snapshot.png", snap * 255)

