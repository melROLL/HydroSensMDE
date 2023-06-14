""""
import OS_function

nex = OS_function.folder_path(('..', "assets", "images", "image_preview.jpg"))
print(nex)

import cv2

def list_cameras():
    # Initialize the VideoCapture object
    cap = cv2.VideoCapture(0)

    # Get the camera names
    cameras = []
    for i in range(10):
        try:
            cap.open(i)
            ret, _ = cap.read()
            if ret:
                cameras.append(f"Camera {i}")
        except:
            pass

    # Release the VideoCapture object
    cap.release()

    # Return the camera names
    return cameras

cameras = list_cameras()
print(cameras)
"""

import analysis_function
import OS_function

# Define the absolute path of the reframed image
image_reframe_path = OS_function.folder_path(("..", "assets", "images", "image_reframe.jpg"))

# Get a list of images from the sample
img_list = analysis_function.split_picture_to_sample(image_reframe_path)

for img in img_list:
    analysis_function.water_absportion_analysis(img)