""" Repository of all the camera functions """

# Import the libraries
import cv2
import os
import sys

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
        # Define the resolution
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # Set exposure time to 1200 milliseconds
        cap.set(cv2.CAP_PROP_EXPOSURE, 1200)
        # Capture a frame
        ret, frame = cap.read()
        # If the picture has been taken
        if frame is not None:
            # Rotate the image to fit to the box
            frame = cv2.rotate(frame, cv2.ROTATE_180)
            # If the picture is for the preview
            if preview:
                # Check if running as an executable
                if getattr(sys, 'frozen', False):
                    # Running as executable
                    executable_dir = os.path.dirname(sys.executable)
                    image_preview_dir = os.path.join(executable_dir, "temp_HydroSens", "images")
                    os.makedirs(image_preview_dir, exist_ok=True)
                    image_preview_path = os.path.join(image_preview_dir, "image_preview.jpg")
                else:
                    # Running in development environment
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    image_preview_path = os.path.join(script_dir, "..", "assets", "images", "image_preview.jpg")

                # Get the absolute path of the image
                #image_preview_path = os.path.join('assets', 'images', 'image_preview.jpg')
                #image_preview_path = OS_function.folder_path(("..", "assets", "images", "image_preview.jpg"))
                # Save the captured image to a file
                cv2.imwrite(image_preview_path, frame)
                # Release the camera
                cap.release()
            else:
                # Save the captured image to a file
                cv2.imwrite(path, frame)
                # Release the camera
                cap.release()
        else:
            # Print an error message in the console
            print("Error: Empty frame.")

