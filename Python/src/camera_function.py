""" Repository of all the camera functions """

import cv2
import os
import pygame.camera

def list_ports():
    pygame.camera.init()
    camlist = pygame.camera.list_cameras()
    pygame.camera.quit()
    return camlist

def take_picture(preview, port, path=None):
    # Initialize the camera
    cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)
    # Capture a frame

    ret, frame = cap.read()

    if preview:
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Construct the relative path to the image file
        image_preview_path = os.path.join(script_dir, "..", "assets", "images", "image_preview.jpg")

        if frame is not None:
            # Save the captured image to a file
            cv2.imwrite(image_preview_path, frame)
            # Release the camera
            cap.release()
        else:
            print("Error: Empty frame.")

