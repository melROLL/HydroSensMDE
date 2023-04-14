""" Repository of all the camera functions """

# Import the libraries
import cv2
import os

# Import the Python functions
import OS_function

# Define all the available cameras
def list_cameras():
    # Initialize a list of cameras
    cameras = []
    # Initialize the first index
    index = 0
    # While we can open another camera
    while True:
        # Create a VideoCapture object for windows
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        # If we can't open the camera
        if not cap.isOpened():
            break
        # Add the name of the camera to the list
        cameras.append(f"Camera {index}")
        # Release the camera
        cap.release()
        # Implement the index
        index += 1
    # Return the list of cameras
    return cameras

# Take picture
def take_picture(preview, port, path=None):
    # If a camera is defined
    if port is not None:
        # Initialize the camera
        cap = cv2.VideoCapture(port, cv2.CAP_DSHOW)
        # Set exposure time to 500 milliseconds
        cap.set(cv2.CAP_PROP_EXPOSURE, 1000)
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

