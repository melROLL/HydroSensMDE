import cv2
# pip3 install opencv-python

import os

# create the folder if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# select the device index for the camera you want to use
# 0 is for the integrated webcam 
device_index = 1

# initialize the camera
cap = cv2.VideoCapture(device_index)

# capture a frame
ret, frame = cap.read()


# capture a frame
ret, frame = cap.read()

# save the captured image to a file in the programefolder
cv2.imwrite("image.jpg", frame)

# save the captured image to a file in the images folder
cv2.imwrite("images/image.jpg", frame)

# release the camera
cap.release()

