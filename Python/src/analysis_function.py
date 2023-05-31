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

# Delete the contour
def remove_contours(path, export_path):
    # Load the image
    img = cv2.imread(path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast of the image
    alpha = 2  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(adjusted, 80, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a new image
    reframe_img = img.copy()

    for contour in contours:
        # Approximate the contour to a polygon
        polygon = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        
        # If the polygon has four sides and is not too small or too large
        if len(polygon) == 4 and cv2.contourArea(polygon) > 10000 and cv2.contourArea(polygon) < 500000:

            # Create a mask with the same shape as the original image
            mask = np.ones_like(reframe_img, dtype=np.uint8) * 255

            # Draw the contours on the mask with a black color
            cv2.drawContours(mask, contours, -1, (0, 0, 0), cv2.FILLED)

            # Invert the mask by subtracting it from a white image
            opposite_mask = cv2.subtract(np.ones_like(reframe_img) * 255, mask)

            # Apply the opposite mask to the image
            reframe_img = cv2.bitwise_and(reframe_img, opposite_mask)

    # Display the new image
    #cv2.imshow('New Image', reframe_img)
    #cv2.waitKey(0)

    # Save the new image to a file
    cv2.imwrite(export_path, reframe_img)

    # Close all windows
    cv2.destroyAllWindows()

# Split the picture into sample
def split_picture_to_sample(path, export_path=None):
    # Load the image
    img = cv2.imread(path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast of the image
    alpha = 1  # Contrast control (1.0-3.0)
    beta = 0  # Brightness control (0-100)
    adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)

    # Apply a threshold to create a binary image
    _, thresh = cv2.threshold(adjusted, 110, 255, cv2.THRESH_BINARY_INV)

    #cv2.imshow('Contours', thresh)
    #cv2.waitKey(0)

    # Find contours in the binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Counter of paper sheet
    counter = 0

    # List of images
    img_list = [] 

    # Loop over the contours and find rectangular shapes
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.05 * cv2.arcLength(contour, True)
        polygon = cv2.approxPolyDP(contour, epsilon, True)
        
        # Check if the polygon has a sufficient number of sides
        if len(polygon) >= 3 and cv2.contourArea(polygon) > 1000 and cv2.contourArea(polygon) < 50000:
            # Increase the counter
            counter += 1

            # Get the bounding rectangle for the polygon
            x, y, w, h = cv2.boundingRect(polygon)
            
            # Draw the contour on the image
            #cv2.drawContours(img, [polygon], -1, (0, 255, 0), 2)
            
            # Display the image with contours
            #cv2.imshow('Contours', img)
            #cv2.waitKey(0)
            
            # Crop the image to the bounding rectangle
            cropped = img[y-50:y+h+50, x-50:x+w+50]
            
            # Display the cropped image
            cv2.imshow('Cropped', cropped)
            cv2.waitKey(0)
            
            # Save the new image to a file
            #cv2.imwrite(export_path+'_'+str(counter)+'.jpg', cropped)
            img_list.append(cropped)

    # Close all windows
    cv2.destroyAllWindows()
    
    # Return the number of paper detected
    return img_list

def water_absportion_analysis(img):
    # Define the number of waterdrop
    number_of_sample = 1

    # Resize the image
    resized_img = cv2.resize(img, (480, 360))

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)

    # Adjust the brightness and contrast of the image
    alpha = 0.9  # Contrast control (1.0-3.0)
    beta = -15  # Brightness control (0-100)
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
        if min_raduis_param > 2:
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

        # If no water drop have been detected
        if circles is None:
            print("No water drop has been detected!")
            break
        
        # If there is the right number of water drop detected
        if circles.shape[0] == number_of_sample:
            # Define the area threshold
            area_threshold = 1200

            # Print the numbers of circles detected.
            #print(f"{circles.shape[0]} water drop has (have) been detected!")

            # For all the elements of the circles
            for (x, y, r) in circles:
                # Calculate the area of the circle
                circle_area = np.pi * r ** 2
                # Check if the area is greater than the threshold
                print(f"The area of the circle is {circle_area:.2f}")
                # Calculate the area of each circle and check if it's greater than the threshold
                if circle_area > area_threshold:
                    print("Water drop absorbed!")
                else:
                    print("No absorption detected!")
            break



