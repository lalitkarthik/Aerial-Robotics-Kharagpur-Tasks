import cv2

def turtle():
    img=cv2.imread("maze.png")
    img_copy=img.copy()
    cv2.imshow("Maze",img_copy)

    cv2.waitKey(0)
    cv2.destroyAllWindows

    def draw_circle(image, coord):
        cv2.circle(image, coord, 2, (230,202,142), -1)

    gray=cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, binary= cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    mask= cv2.bitwise_not(binary)

    centre_x=440
    centre_y=330
    # centre_x=20
    # centre_y=30
    while True:

        draw_circle(img_copy, (centre_x, centre_y))
        print(f"x_coord:{centre_x}, y_coord:{centre_y}")

        cv2.imshow("Moving Circle", img_copy)

        key = cv2.waitKey(1)

        new_centre_x = centre_x
        new_centre_y = centre_y
        if key == ord('w'):
            new_centre_y -= 1
        elif key == ord('s'):
            new_centre_y += 1
        elif key == ord('a'):
            new_centre_x -= 1
        elif key == ord('d'):
            new_centre_x += 1

        # Check if the new position is within the allowed area
        if mask[new_centre_y, new_centre_x] != 255:
            centre_x, centre_y = new_centre_x, new_centre_y

        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    return None