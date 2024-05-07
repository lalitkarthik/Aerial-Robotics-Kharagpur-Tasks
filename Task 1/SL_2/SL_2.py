import numpy as np
import cv2
import matplotlib.pyplot as plt

#setting the parameter after Hit and Trial
kernel_size=20

#Importing the images
left=cv2.imread("left.png")
right=cv2.imread("right.png")

def sobel_processing(image):

    sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    return gradient_magnitude.astype(np.uint8)

#Converting the image to GrayScale
left_gray=cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
right_gray=cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

#Applying Gaussian BLur
left_gray=cv2.GaussianBlur(left_gray, (7,7), 0)
right_gray=cv2.GaussianBlur(right_gray, (7,7), 0)

#Performing sobel operation
left_sobel=sobel_processing(left_gray)
right_sobel=sobel_processing(right_gray)

#Addition of padding
def add_padding(image, kernel_size):
    padding_size= kernel_size//2
    padded_image = cv2.copyMakeBorder(image, padding_size, padding_size, padding_size, padding_size, cv2.BORDER_CONSTANT, value=0)
    return padded_image


def disparity_construction(left_img, right_img, kernel_size, max_disparity=30):
    
    #Padding before processing
    left_padded=add_padding(left_img, kernel_size)
    right_padded=add_padding(right_img, kernel_size)

    height, width= left_padded.shape
    disparity_map=np.zeros((height, width), dtype=np.float32)

    offset= kernel_size//2

    print("Processing...... Please wait for a minute or two.")

    for y in range(offset, height - offset):
        for x in range(offset, width - offset):

            min_cost=float("inf") #Setting the cost to infinity initially
            best_disparity=0
        
            search_range = min(x - offset, max_disparity) #Setting the proper serch range aprt
            left_part=left_padded[y-offset:y+offset+1, x-offset:x+offset+1]

            for d in range(search_range):
                right_part=right_padded[y-offset:y+offset+1, (x-d)-offset:(x-d)+offset+1]

                cost=np.sum((left_part-right_part)**2) #SSD Calculation

                if(cost<min_cost):
                    min_cost=cost
                    best_disparity= d
    
            disparity_map[y,x]=best_disparity

    
    return disparity_map

#Function for constructing Depth map from Disparity map
def depth_map_construction(disparity_map):

    normalized_disp=(disparity_map/np.max(disparity_map))
    height, width= normalized_disp.shape
    depth_map= np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            r= int(255 * (normalized_disp[y,x]))
            b= int(255 * (1-(normalized_disp[y,x])))
            depth_map[y,x]= (b, 0, r)

    return depth_map


#Processing Disparity map for Depth map construction
disparity_map=disparity_construction(left_sobel, right_sobel, kernel_size)

disparity_map_normalized= (disparity_map/ np.max(disparity_map))*255
disparity_map_normalized= disparity_map_normalized.astype(np.uint8)

depth_map=depth_map_construction(disparity_map_normalized)
height, width=depth_map.shape[:2]
depth_map=depth_map[(kernel_size//2+1):height-(kernel_size//2),(kernel_size//2)+1:width-(kernel_size//2)]

print("Done!!")

cv2.imwrite("Depth_Map.png", depth_map)

cv2.imshow('Depth Map', depth_map)
cv2.waitKey(0)
cv2.destroyAllWindows()
