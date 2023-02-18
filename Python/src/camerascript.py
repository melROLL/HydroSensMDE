import cv2
# pip3 install opencv-python

# initialize the camera
cap = cv2.VideoCapture(0)

# capture a frame
ret, frame = cap.read()

# save the captured image to a file
cv2.imwrite("image.jpg", frame)

# release the camera
cap.release()
