"""HydroSens GUI"""

# Import the necessary libraries
import os
import cv2
import time
import threading
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk, Image

# Import the Python functions
import OS_function
import camera_function
import analysis_function

# Create a class of customtkinter
class HydroSensApp(ctk.CTk):
    # Initialization
    def __init__(self):
        super().__init__()
        # Title of the window
        self.title("Hydrosens System")
        # Dimension of the window
        self.geometry("1280x785")
        # Appearance of the window
        ctk.set_appearance_mode("system")
        # Color of the window
        ctk.set_default_color_theme("dark-blue")

        # Creation of a customtkinter frame
        self.frame = ctk.CTkFrame(master=self)
        # Define a pack for widgets
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Create columns in the frame
        self.frame.columnconfigure(0, weight=1, minsize=200)
        self.frame.columnconfigure(1, weight=1, minsize=200)
        self.frame.columnconfigure(2, weight=1, minsize=200)
        self.frame.columnconfigure(3, weight=1, minsize=200)

        # Creation of a label widget
        self.title = ctk.CTkLabel(master=self.frame, text="HydroSens System", \
            font=("Helvetica", 24, "bold"))
        # Set up the position of the label widget
        self.title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        # Creation of a entry widget
        self.project_name = ctk.CTkEntry(master=self.frame, \
            placeholder_text="Name of test project", font=("Helvetica", 14))
        # Set up the position of the entry widget
        self.project_name.grid(row=1, column=0, columnspan=4, padx=15, pady=10, sticky="ew")

        # Creation of a entry widget        
        self.duration_between_pictures = ctk.CTkEntry(master=self.frame, \
            placeholder_text="Number of seconds between each picture", font=("Helvetica", 14),)
        
        # Extract the text color
        initial_color = self.duration_between_pictures.cget("fg_color")

        # Modify the appearance of the entry
        self.duration_between_pictures.bind("<KeyRelease>", lambda event: self.format_numeric_duration(self.frame, \
            self.duration_between_pictures.get(), initial_color))

        # Set up the position of the entry widget
        self.duration_between_pictures.grid(row=2, column=0, columnspan=4, padx=15, pady=10, sticky="ew")

        # Creation of a entry widget
        self.duration_max = ctk.CTkEntry(master=self.frame, \
            placeholder_text="Duration of the experimentation in minutes", font=("Helvetica", 14))
        
        # Modify the appearance of the entry
        self.duration_max.bind("<KeyRelease>", lambda event: self.format_numeric_max(self.frame, \
            self.duration_max.get(), initial_color))

        # Set up the position of the entry widget
        self.duration_max.grid(row=3, column=0, columnspan=4, padx=15, pady=10, sticky="ew")

        # Create a variable for the export path
        self.folder_path=tk.StringVar()

        # Create the variable which contains the camera choosen
        self.camera_box_var = ctk.StringVar()
        # Launch the function that handles the camera choice
        self.gui_camera_port(self.frame)

        # Creation of a button widget to update the camera function
        self.button_update_cam = ctk.CTkButton(master=self.frame, text="Update",font=("Helvetica", 14), \
            command=lambda: self.gui_camera_port(self.frame))
        # Set up the position of the button widget
        self.button_update_cam.grid(row=4, column=3, padx=10, pady=10, sticky="ew")

        # Creation of a button widget to select an output folder
        self.button_path_export = ctk.CTkButton(master=self.frame, text="Select an output folder", \
            font=("Helvetica", 14), command=lambda: self.folder_path.set(self.open_folder(self.frame)))
        # Set up the position of the button widget
        self.button_path_export.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Launch the function that handles the image display
        self.display_image(self.frame)

        # Create the variable which contains an arbitrary value
        self.to_the_end = ctk.StringVar(value="wait")
        # Creation of a checkbox widget to select the mode of processing
        self.checkbox_to_the_end = ctk.CTkCheckBox(master=self.frame, text="Waiting for the end", \
            variable=self.to_the_end, onvalue="wait", offvalue="auto")
        # Set up the position of the button widget
        self.checkbox_to_the_end.grid(row=7, columnspan=2, column=3, padx=15, pady=10, sticky="w")

         # Create the variable which contains an arbitrary value
        self.check_sys_color = ctk.StringVar(value="on")
        # Creation of a checkbox widget to select the theme of the window
        self.checkbox_sys_color = ctk.CTkCheckBox(master=self.frame, text="Theme", command=self.user_theme, \
            variable=self.check_sys_color, onvalue="on", offvalue="off")
        # Set up the position of the button widget
        self.checkbox_sys_color.grid(row=10, columnspan=2, column=0, padx=15, pady=10, sticky="w")

    # Choice of the camera in the GUI
    def gui_camera_port(self, frame):
        # Reset the value of the camera
        self.camera_box_var.set('')
        # Get the available cameras
        self.cameras = camera_function.list_cameras()
        # If a camera has been detected
        if len(self.cameras) != 0:
            # Put the first camera as the initial choice
            self.camera_box_var.set(self.cameras[0])
            # Creation of a combobox widget
            camera_box = ctk.CTkComboBox(master=frame, values=self.cameras, variable=self.camera_box_var)
            # Set up the position of the combobox widget
            camera_box.grid(row=4, column=0, columnspan=3, padx=15, pady=10, sticky="ew")

            # Creation of a button widget to take a preview picture
            self.button_preview = ctk.CTkButton(master=self.frame, text="Preview", font=("Helvetica", 14), \
                command=lambda: (camera_function.take_picture(True, self.cameras.index(self.camera_box_var.get())), \
                    self.display_image(self.frame)))
            # Set up the position of the button widget
            self.button_preview.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

            # Creation of a button widget to take launch the analysis
            self.button_execute = ctk.CTkButton(master=self.frame, text="Launch", font=("Helvetica", 14), \
                command=lambda: self.execute(self.project_name.get(), self.duration_between_pictures.get(), self.duration_max.get(), \
                    self.cameras.index(self.camera_box_var.get()), self.folder_path.get(), self.to_the_end.get()))
            # Set up the position of the button widget
            self.button_execute.grid(row=6, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

        else:
            # Creation of a label widget
            camera_box = ctk.CTkLabel(master=self.frame, \
                text="No camera detected! Please check the connection with the camera and retry.", font=("Helvetica", 14))
            # Set up the position of the label widget
            camera_box.grid(row=4, column=0, columnspan=3, padx=15, pady=10, sticky="ew")
            # Creation of a label widget
            button_preview = ctk.CTkLabel(master=self.frame, text="", font=("Helvetica", 14))
            # Set up the position of the label widget to hide the button
            button_preview.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

    # Display an image in the GUI
    def display_image(self, frame):
        # Create a new frame
        image_container = ctk.CTkFrame(master=frame)
        # Set up the position of the frame
        image_container.grid(rowspan=4, row=7, columnspan=4, column=0, padx=10, pady=10, sticky="ns")
        # Get the absolute path of the image
        image_preview_path = OS_function.folder_path(("..", "assets", "images", "image_preview.jpg"))

        # Try to display the image
        try:
            # Open the image
            image_preview = Image.open(image_preview_path)

            # Resize the image to a new width and height
            new_width = 500
            new_height = round(new_width*0.75)
            resized_image = image_preview.resize((new_width, new_height))

            # Create a Tkinter-compatible PhotoImage object
            tk_image_preview = ImageTk.PhotoImage(resized_image)

            # Create a label widget and 
            label_preview = tk.Label(image_container, image=tk_image_preview)
            # Pack the image inside the spacer frame
            label_preview.image = tk_image_preview
            label_preview.pack()

        # If there is no image
        except IOError:
            print("No picture to print.")

    # Select an output path and show it in the GUI
    def open_folder(self, frame):
        # Ask the user to select a path
        folder_path = filedialog.askdirectory(title="Select an output folder")
        # If the path has been choosen
        if folder_path:
            # Print the path in the console
            print(f"Selected folder: {folder_path}")
            # Modify the appearance of the button to print the path
            self.button_path_export.configure(text=str(folder_path), width=10, \
                fg_color="purple", font=("Helvetica", 14))
            return folder_path
    
    # Define the desired variable format
    def format_numeric_duration(self, frame, input_text, initial_color):
        # If the input_text is not numeric
        if not input_text.isnumeric():
            # Modify the appearance of the button
            self.duration_between_pictures.configure(width=10, fg_color="#5C2F2F", font=("Helvetica", 14))
        else:
            self.duration_between_pictures.configure(width=10, fg_color=initial_color, font=("Helvetica", 14))
    
    # Define the desired variable format
    def format_numeric_max(self, frame, input_text, initial_color):
        # If the input_text is not numeric
        if not input_text.isnumeric():
            # Modify the appearance of the button
            self.duration_max.configure(width=10, fg_color="#5C2F2F", font=("Helvetica", 14))
        else:
            # Modify the appearance of the button
            self.duration_max.configure(width=10, fg_color=initial_color, font=("Helvetica", 14))

    # Select the theme of the window
    def user_theme(self):
        # Print the choice in the console
        print("System color dark:", self.check_sys_color.get())
        # If the button value is on 
        if self.check_sys_color.get()=="on":
            # Define the appearance in Dark mode
            ctk.set_appearance_mode("dark")
        else:
            # Define the appearance in Light mode
            ctk.set_appearance_mode("light")
    
    def execute(self, name, duration, duration_max, camera_port, export_path, wait_end):
        # Remove the blank at the begenning and at the end
        name = name.strip()
        export_path = export_path.strip()

        # If all the entries are correctly filled
        if name == "" or not duration.isnumeric() or not duration_max.isnumeric() or export_path == "None" or export_path == "":
            # Create a message box
            tkmessagebox = tk.messagebox
            # Create a message box instance and display it
            tkmessagebox.showinfo("Value error", "Please make sure to enter the right values.")
        else:
            # Create a new thread to display the processing window
            t1 = threading.Thread(target=self.processing_window)
            # Start the process
            t1.start()
            
            # Create a new thread to run the processing function
            t2 = threading.Thread(target=self.processing, args=(name, float(duration), float(duration_max), camera_port, export_path, wait_end))
            # Start the process
            t2.start()

    def processing_window(self):
        # Create a message box
        tkmessagebox = tk.messagebox
        # Create a message box instance and display it
        tkmessagebox.showinfo("Loading", "The treatment is processing...")

    def finished_window(self):
        # Create a message box
        tkmessagebox = tk.messagebox
        # Create a message box instance and display it
        tkmessagebox.showinfo("Finished", "The treatment is finished.")

    def error_window(self):
        # Create a message box
        tkmessagebox = tk.messagebox
        # Create a message box instance and display it
        tkmessagebox.showinfo("Error", "An error occured during the processing.")
    
    def processing(self, name, duration, duration_max, camera_port, export_path, wait_end):
        # Compute the number of iteration
        nb_iteration_max = round(60*duration_max/duration)+1
        # Initialize the number of iteration
        nb_iteration = 0
        # Loop for the specified number of seconds
        start_time = time.time()
        # Define the folder path to export
        export_path_txt = export_path+'/'+name+'/'+'Results.txt'
        export_path = export_path+'/'+name+'/'+'Picture'+'-'
        export_path = export_path[0].lower() + export_path[1:].replace('/', '\\')
        
        # Check if the directory exists
        if not os.path.exists(os.path.dirname(export_path)):
            try:
                # Create the folder
                os.makedirs(os.path.dirname(export_path))
            except OSError as e:
                # Show an error message
                print("Error: Unable to create directory:", e)
                # Display the error window
                self.error_window()
                return
        
        # Create a list of image
        img_list = []

        # Create a text file
        OS_function.create_text_file(export_path_txt)

        # Launch a loop
        while True:
            # Record the start time of the iteration
            start_time = time.time()                

            try:
                # Take picture in the desired folder
                camera_function.take_picture(False, camera_port, export_path+str(nb_iteration)+ \
                    '-'+str(int(nb_iteration*duration/60))+'m'+'-'+str(int((nb_iteration*duration) % 60))+ \
                        's'+'.jpg')
                
                # Define the absolute path of the reframed image
                image_reframe_path = OS_function.folder_path(("..", "assets", "images", "image_reframe.jpg"))
                
                # Remove the boarder
                analysis_function.remove_contours(export_path+str(nb_iteration)+ \
                    '-'+str(int(nb_iteration*duration/60))+'m'+'-'+str(int((nb_iteration*duration) % 60))+ \
                        's'+'.jpg', image_reframe_path)
                #analysis_function.remove_contours('c:\\Users\\trist\\Downloads\\P4A\\test10\\Picture-1-0m-20s.jpg', image_reframe_path)
                #analysis_function.remove_contours('c:\\Users\\trist\\Downloads\\P4A\\test10\\Picture-2-1m-0s.jpg', image_reframe_path)
                #analysis_function.remove_contours('c:\\Users\\trist\\Downloads\\P4A\\test11\\Picture-2-0m-40s.jpg', image_reframe_path)
                #analysis_function.remove_contours('c:\\Users\\trist\\Downloads\\P4A\\test14\\Picture-0-0m-0s.jpg', image_reframe_path)
                #analysis_function.remove_contours('c:\\Users\\trist\\Downloads\\P4A\\test20\\Picture-0-0m-0s.jpg', image_reframe_path)
                
                # Define the absolute path of the reframed image
                #image_split_path = OS_function.folder_path(("..", "assets", "images", "image_split"))
                
                # Get a list of images from the sample
                img_list = analysis_function.split_picture_to_sample(image_reframe_path)

                # Write in the text result file
                OS_function.write_to_text_file(export_path_txt, "\n\nPicture number "+str(nb_iteration)+ \
                    " for a duration of "+str(int(nb_iteration*duration/60))+"m and "+str(int((nb_iteration*duration) % 60))+ \
                        "s:")

                # Define an index for the sample
                counter = 0

                # Create a list of results
                list_results = []

                # Define a stop boolean
                stop = False

                # For all the image of samples
                for img in img_list:
                    # Implement a counter for the number of the sample
                    counter += 1
                    # Detect if the absorption occured
                    result = analysis_function.water_absportion_analysis(img)

                    # Add the results to the list
                    list_results.append(result)

                    # If the paper sample has absorbed the water
                    if result == 0:
                        # Write the corresponding line in the result file text
                        OS_function.write_to_text_file(export_path_txt, "\nSample number "+str(counter)+": absorbed.")
                    elif result == 1:
                        # Write the corresponding line in the result file text
                        OS_function.write_to_text_file(export_path_txt, "\nSample number "+str(counter)+": not absorbed.")
                    else:
                        # Write the corresponding line in the result file text
                        OS_function.write_to_text_file(export_path_txt, "\nSample number "+str(counter)+": no water detected.")

                    # Show the split images
                    #cv2.imshow('Cropped', img)
                    #cv2.waitKey(0)

                # If all the paper have  absorbed the water and the end is on automatic mode 
                if all( result == 0 for result in list_results) and wait_end == "auto":
                    # Define a stop variable to stop the execution
                    stop = True
                    # Write the corresponding line in the result file text
                    OS_function.write_to_text_file(export_path_txt, "\n\nProgram stopped.")

            except Exception as e:
                # Show an error message
                print("Error:", e)
                # Display the error window
                self.error_window()
                break

            # Add an iteration
            nb_iteration += 1

            # If the number of iterations has reached the maximum
            if nb_iteration == nb_iteration_max or stop:
                # Display the finished message
                self.finished_window()
                # Leave the loop
                break
                
            # Record the end time of the iteration
            end_time = time.time()  
                
            # Compute the duration since the start of the iteration
            elapsed_time = end_time - start_time
                
            # If there is still time left in the interval
            if elapsed_time < duration:
                # Wait
                time.sleep(duration - elapsed_time)

# Execute the GUI
def main():
    app = HydroSensApp()
    app.mainloop()

if __name__ == "__main__":
    main()
