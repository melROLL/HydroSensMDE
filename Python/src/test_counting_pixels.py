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

