""" Repository of all the OS functions """

# Import the libraries
import os 

# Define the absolute path from a tuple of separate path
def folder_path(path_detailed):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the relative path to the image file
    absolute_path = os.path.join(script_dir, *path_detailed)
    # Return the absolute path
    return absolute_path

