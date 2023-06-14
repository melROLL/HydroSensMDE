from PIL import Image
import numpy as np

#load the image 
image = Image.open("image.jpg")
image_np = np.array(image)

#image to 1D array 
image_flat = image_np.reshape(-1, 3)

#count the ocurence of each pixel by color
unique_colours, counts = np.unique(image_flat, axis=0, return_counts=True)


#display the result 
for color, count in zip(unique_colours, counts):
    print(f"Color: {color}, Count: {count}")

# Calculate the total number of pixels in the image
total_pixels = image_np.shape[0] * image_np.shape[1]

# Calculate the percentage of each color
for color, count in zip(unique_colours, counts):
    percentage = (count / total_pixels) * 100
    print(f"Color: {color}, Percentage: {percentage:.2f}%")