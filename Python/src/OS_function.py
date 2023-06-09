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

# Create a text file
def create_text_file(file_path):
    try:
        # Open the file in write mode)
        with open(file_path, 'w') as file:
            # Perform any necessary operations on the file
            file.write('HydroSens results file.')

        print(f"The file '{file_path}' has been created successfully.")

    except Exception as e:
        print(f"An error occurred while creating the file: {str(e)}")

# Write on a text file
def write_to_text_file(file_path, content):
    # Check if the file already exists
    file_exists = os.path.isfile(file_path)

    # Open the file in append mode or create a new file if it doesn't exist
    with open(file_path, 'a' if file_exists else 'w') as file:
        # Write the content to the file
        file.write(content)

