import cv2
import numpy as np

def sobel_edge_detection(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Define Sobel kernels
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])

    sobel_y = np.array([[1, 2, 1],
                        [0, 0, 0],
                        [-1, -2, -1]])

    # Convolve image with Sobel kernels
    grad_x = cv2.filter2D(gray_image, -1, sobel_x)
    grad_y = cv2.filter2D(gray_image, -1, sobel_y)

    # Compute gradient magnitude
    grad_mag = np.sqrt((grad_x ** 2.0) + (grad_y ** 2.0))
    
    # Normalize gradient magnitude 
    grad_mag *= 255.0 / grad_mag.max()

    theta=np.arctan2(grad_y,grad_x)

    return np.squeeze(grad_mag), np.squeeze(theta)


#Function for non_max_suppression
def non_max_suppression(img,theta):
    m,n= img.shape
    z=np.zeros((m,n),dtype=np.int32)

    angle =theta*180.0/np.pi #Converting to radians
    angle[angle<0]+= 180 #making angles positiv

    for i in range(1,m-1):
        for j in range(1,n-1):
            q=255
            r=255

            # Angle 0 Horizontal edges
            if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                r = img[i, j-1]  
                q = img[i, j+1] 

            # Angle 45:Diagonal edges from bottom left to top right
            elif (22.5 <= angle[i, j] < 67.5):
                r = img[i-1, j+1]
                q = img[i+1, j-1] 

            # Angle 90: Vertical edges
            elif (67.5 <= angle[i, j] < 112.5):
                r = img[i-1, j]  
                q = img[i+1, j] 

            # Angle 135: Diagonal edges from bottom right to top left
            elif (112.5 <= angle[i, j] < 157.5):
                r = img[i+1, j+1]  
                q = img[i-1, j-1]  

            if(img[i,j]>=q and img[i,j]>=r):
                z[i,j]=img[i,j]
            else:
                z[i,j]=0
    
    return z

def threshold_hysterisis(img, high, low):

    m,n=img.shape

    res=np.zeros((m,n), dtype=np.int32)

    strong=np.int32(255)
    weak=np.int32(25)

    strong_i, strong_j = np.where(img >= high)
    weak_i, weak_j = np.where((img <= high) & (img >= low))

    res[strong_i, strong_j] = strong
    res[weak_i, weak_j] = weak

    #Hysterisis
    for i in range(1, m-1):
        for j in range(1, n-1):
            if (res[i, j] == weak):
                #conditions o check if the weak edge is connected to strong edges
                if (
                    (res[i+1,j-1] == strong) or (res[i+1, j] == strong) or    
                    (res[i+1,j+1] == strong) or (res[i, j-1] == strong) or
                    (res[i,j+1] == strong) or (res[i-1, j-1] == strong) or
                    (res[i-1,j] == strong) or (res[i-1, j+1] == strong)
                ):
                    res[i,j] = strong
                else:
                    res[i,j] = 0

    return res


img=cv2.imread("./Table.png")
#Canny part
grad, theta= sobel_edge_detection(img)
edge=non_max_suppression(grad, theta)
edges=threshold_hysterisis(edge, 200,255)
edges = np.uint8(edges)

cv2.imwrite("./Edge_for_table.png", edges)
height, width = img.shape[0],img.shape[1]

cv2.imshow("Edges",edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=5, minLineLength=10, maxLineGap=200)
count=0
if lines is not None:
    for line in lines:
        line_image = img.copy()
        x1, y1, x2, y2 = line[0]
        if x2 != x1:
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            
            # Calculate intersections
            y_at_beginning = int(c)
            y_at_end = int(m *width + c)
            x_at_beginning = int((-c) / m)
            x_at_end = int((height -c) / m)
            
            # Determine points to draw line
            start_point = (0, y_at_beginning) if 0 <= y_at_beginning <= height else (x_at_beginning, 0)
            end_point = (width, y_at_end) if 0 <= y_at_end <= height else (x_at_end, height)
            
            # Draw the extended line
            cv2.line(line_image, start_point, end_point, (0, 255, 0), 3)
            cv2.circle(line_image, (x1,y1), 5, (0,255,0),-1 )
            cv2.circle(line_image, (x2,y2), 5, (0,255,0),-1 )
            if(count==0):
                cv2.imwrite("./Table_edge.png", line_image)
            cv2.imshow('Lines Detected', line_image)
            cv2.waitKey(1000)
            count+=1

cv2.destroyAllWindows()
