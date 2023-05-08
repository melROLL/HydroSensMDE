""" Repository of all the analysis functions """

"""
# sample code using Python and TensorFlow library to train a CNN to detect if the paper is wet or not 
# thisi=s from chat gpt 
# rthis file is not compiling yet 

import tensorflow as tf
from tensorflow.keras import layers

# load dataset and prepare data

# define the model
model = tf.keras.Sequential([
  layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
  layers.MaxPooling2D(),
  layers.Conv2D(64, (3,3), activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(1, activation='sigmoid')
])

# compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# train the model
model.fit(train_data, epochs=10, validation_data=val_data)

# evaluate the model
test_loss, test_acc = model.evaluate(test_data)
print('Test accuracy:', test_acc)
"""

import cv2
import numpy as np

# Determine if the absorption occured
def water_absportion_analysis(path):
    # Load the image
    img = cv2.imread(path)

    # Define the number of waterdrop
    number_of_sample = 1

    # Resize the image
    resized_img = cv2.resize(img, (640, 480))

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast of the image
    alpha = 2.5  # Contrast control (1.0-3.0)
    beta = 60  # Brightness control (0-100)
    gray_img = cv2.convertScaleAbs(gray_img, alpha=alpha, beta=beta)

    cv2.imshow("Circles", gray_img)
    cv2.waitKey(0)

    # Define the parameters
    gray_param_1, gray_param_2 = 10, 30
    circle_param_1, circle_param_2 = 22, 20 
    min_raduis_param = 10

    while True:
        # Apply Canny edge detection to the grayscale image
        edges = cv2.Canny(gray_img, gray_param_1, gray_param_2)

        # Change the values of the gray parameters
        gray_param_1 += 1
        gray_param_2 += 5

        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Apply Hough Circle Transform
        circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1, 20, param1=circle_param_1, param2=circle_param_2, minRadius=min_raduis_param, maxRadius=0)

        # Change the circle parameters
        circle_param_1 += 1
        circle_param_2 += 1
        if min_raduis_param < 2:
            min_raduis_param -= 2
        
        # Draw circles on the original image
        circle_img = resized_img.copy()
        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")
            for (x, y, r) in circles:
                cv2.circle(circle_img, (x, y), r, (0, 255, 0), 2)
        
        # Display the result
        cv2.imshow("Circles", circle_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if circles.shape[0] == number_of_sample:
            break

    # Display the result
    cv2.imshow("Circles", circle_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Define the area threshold
    area_threshold = 850

    # Print the numbers of circles detected.
    print(f"{circles.shape[0]} water drop has (have) been detected!")

    # Calculate the area of each circle and check if it's greater than the threshold
    if circles is not None:
        for (x, y, r) in circles:
            # Calculate the area of the circle
            circle_area = np.pi * r ** 2
            # Check if the area is greater than the threshold
            print(f"The area of the circle is {circle_area:.2f}")
            if circle_area > area_threshold:
                print("Water drop absorbed!")
            else:
                print("No absorption detected!")

# Delete the contours
def remove_contours(path):
    # Load the image
    img = cv2.imread(path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast of the image
    alpha = 2  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(adjusted, 65, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a new image
    new_img = img.copy()

    # Loop over the contours and find rectangular shapes
    for contour in contours:
        # Approximate the contour to a polygon
        polygon = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        
        # If the polygon has four sides and is not too small or too large
        if len(polygon) == 4 and cv2.contourArea(polygon) > 10000 and cv2.contourArea(polygon) < 500000:
            # Draw the contour on the new image
            cv2.drawContours(new_img, [polygon], 0, (255, 255, 255), cv2.FILLED)

    # Display the new image
    cv2.imshow('New Image', new_img)
    cv2.waitKey(0)

    # Save the new image to a file
    cv2.imwrite('Photo/box/new_img.jpg', new_img)

    # Close all windows
    cv2.destroyAllWindows()


# Split the picture into sampled
def split_picture_to_sample(path):
    # Load the image
    img = cv2.imread(path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast of the image
    alpha = 0.8  # Contrast control (1.0-3.0)
    beta = 60  # Brightness control (0-100)
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(adjusted, 130, 255, cv2.THRESH_BINARY_INV)

    # Display the binary image
    cv2.imshow('Binary', thresh)
    cv2.waitKey(0)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over the contours and find rectangular shapes
    for contour in contours:
        # Approximate the contour to a polygon
        polygon = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        
        # If the polygon has four sides and is not too small or too large
        if len(polygon) == 4 and cv2.contourArea(polygon) > 10000 and cv2.contourArea(polygon) < 500000:
            # Get the bounding rectangle for the polygon
            x, y, w, h = cv2.boundingRect(polygon)
            
            # Crop the image to the bounding rectangle
            cropped = img[y-100:y+h+100, x-100:x+w+100]
            
            # Display the cropped image
            cv2.imshow('Cropped', cropped)
            cv2.waitKey(0)
            
            # Save the new image to a file
            cv2.imwrite('Photo/box/final.jpg', cropped)

    # Close all windows
    cv2.destroyAllWindows()

