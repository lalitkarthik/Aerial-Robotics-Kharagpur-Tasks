import numpy as np
import cv2
import random

class FiniteStateMachine:
    def __init__(self):
        self.R = np.array(self.random_permutation(256, "R"))
        self.G = np.array(self.random_permutation(256, "G"))
        self.B = np.array(self.random_permutation(256, "B"))
        self.faces_used = {'R': set(), 'G': set(), 'B': set()}
        self.faces_cost = {'R': 20, 'G': 20, 'B': 20}
        self.change = 0
        self.input_angles = None
        self.coordinates= None

    def random_permutation(self, n, phase):
        arr = np.array(range(n))
        random.shuffle(arr)
        arr=arr.reshape(16,16)
        color_list = np.zeros((16, 16, 3), dtype=np.uint8)  # Initialize color list as a numpy array

        if phase == "R":
            color_list[:, :, 2] = arr  # Assign values to the R channel
        elif phase == "G":
            color_list[:, :, 1] = arr  # Assign values to the G channel
        else:
            color_list[:, :, 0] = arr  # Assign values to the B channel

        return color_list
    
    def input_coordinates(self):
        x = int(input("Enter the x coordinate (0-15): "))
        y = int(input("Enter the y coordinate (0-15): "))
        z = int(input("Enter the z coordinate (0-15): "))
        return (x, y, z)

    def input_rotation(self):
        angle = int(input("Enter rotation angle (0, 90, 180, 270): "))
        return angle

    def rotate_image(self, image, angle):
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        #Predefined function to rotate
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_image = cv2.warpAffine(image, rotation_matrix, (w, h))
        return rotated_image
    
    def show_image(self, image, name):
        resized_image = cv2.resize(image, (400, 400), interpolation=cv2.INTER_NEAREST).astype(np.uint8)
        cv2.imshow(f"{name} Phase", resized_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def calculate_intensity(self, x, y, z):
        RG = np.zeros((16, 16, 3), dtype=np.uint8)
        GB = np.zeros((16, 16, 3), dtype=np.uint8)
        BR = np.zeros((16, 16, 3), dtype=np.uint8)
        R_for_calc=self.R[:, :, 2]
        G_for_calc=self.G[:, :, 1]
        B_for_calc=self.B[:, :, 0]

        for p in range(16):
            for q in range(16):
                RG[p, q] = [R_for_calc[x][p], G_for_calc[y][q], 0]
                GB[q, p] = [0, G_for_calc[y][q], B_for_calc[z][p]]
                BR[p, q] = [R_for_calc[x][p], 0, B_for_calc[z][q]]
        
        return RG, GB, BR
    
    def take_payment(self):
        total_cost = sum(self.faces_cost.values())
        payment = int(input(f"Total cost is {total_cost}. Enter payment: "))
        return payment

    def handle_payment(self, payment):
        if payment >= 60:
            print("Showing all images.")
            self.show_image(self.R, "R")
            self.show_image(self.G, "G")
            self.show_image(self.B, "B")
            self.show_image(self.RG, "RG")
            self.show_image(self.GB, "GB")
            self.show_image(self.BR, "BR")
        elif 20 <= payment < 60:
            choice = input("Enter faces to show ('RG' or 'GB BR'): ").split()
            for face in choice:
                if face == 'RG':
                    self.show_image(self.RG, "RG")
                elif face == 'GB':
                    self.show_image(self.GB, "GB")
                elif face == 'BR':
                    self.show_image(self.BR, "BR")
        else:
            print("Payment is not sufficient. Returning change.")
            self.change = payment

    def validate_row_usage(self):
        for face, rows in self.faces_used.items():
            if len(rows) > 3:
                print(f"Row usage for {face}-face is invalid. Please choose different rows.")
                return False
        return True
    
    def reset_row_usage(self):
        for face in self.faces_used:
            self.faces_used[face] = set()

    def input_state(self):
        self.coordinates = self.input_coordinates()
        self.input_angles = (self.input_rotation(), self.input_rotation(), self.input_rotation())
        return 'Processing'
    
    def processing_state(self):
        x, y, z = self.coordinates
        self.RG, self.GB, self.BR = self.calculate_intensity(x, y, z)
        self.RG = self.rotate_image(self.RG, self.input_angles[0])
        self.GB = self.rotate_image(self.GB, self.input_angles[1])
        self.BR = self.rotate_image(self.BR, self.input_angles[2])
        return 'Payment'
    
    def payment_state(self):
        payment = self.take_payment()
        self.handle_payment(payment)
        if self.change:
            print(f"Change returned: {self.change}")
        return 'Validation'
    
    def validation_state(self):
        if self.validate_row_usage():
            return 'End'
        else:
            self.reset_row_usage()
            return 'Input'
        
    def run(self):
        state_actions = {
            'Start': lambda: 'Input',
            'Input': self.input_state,
            'Processing': self.processing_state,
            'Payment': self.payment_state,
            'Validation': self.validation_state,
            'End': lambda: None
        }
        state = 'Start'
        while state != 'End':
            state = state_actions[state]()
        print("Process completed.")

machine=FiniteStateMachine()
machine.run()
