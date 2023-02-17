import cv2
import os

def getPicture():
    # Start the camera device
    cap = cv2.VideoCapture(0)

    # Capture the image
    ret, frame = cap.read()

    # Image directory
    directory = r'C:\Users\trist\Downloads'
    
    # Change the current directory 
    # to specified directory 
    os.chdir(directory)

    # Save the image
    cv2.imwrite("image.jpg", frame)

    # Release the camera
    cap.release()




getPicture()