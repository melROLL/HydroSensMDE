import cv2
import os
# pip3 install opencv-python

# create the folder if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")
    

#find a webcam 
for i in range(10):
    cap = cv2.VideoCapture(i)
    if cap.read()[0]:
        print(f"Camera {i} is available")
        cap.release()

# select the device index for the camera you want to use 0 is the default webcam
device_index = 0

# initialize the camera
cap = cv2.VideoCapture(device_index)

# capture a frame
ret, frame = cap.read()
# save the captured image to a file
cv2.imwrite("imagetest.jpg", frame)
# save the captured image to a file in the images folder
ret, frame = cap.read()
cv2.imwrite("images/image.jpg", frame)

# release the camera
cap.release()
