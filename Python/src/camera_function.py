""" Repository of all the camera functions """

# Import the libraries
import cv2
import os
import pygame.camera

# Import the Python functions
import OS_function

# Define all the available cameras
def list_ports():
    # Initialize the connexion
    pygame.camera.init()
    # Get the list of available cameras
    camlist = pygame.camera.list_cameras()
    # Quit the module
    pygame.camera.quit()
    # Return the list of cameras
    return camlist

# Take picture
def take_picture(preview, port, path=None):
    # Initialize the camera
    cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)
    # Capture a frame
    ret, frame = cap.read()
    # If the picture has been taken
    if frame is not None:
        # If the picture is for the preview
        if preview:
            # Get the absolute path of the image
            image_preview_path = OS_function.folder_path(("..", "assets", "images", "image_preview.jpg"))
            # Save the captured image to a file
            cv2.imwrite(image_preview_path, frame)
            # Release the camera
            cap.release()
    else:
        # Print an error message in the console
         print("Error: Empty frame.")

