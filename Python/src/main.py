"""HydroSens GUI"""

# Import the necessary libraries
import os
import cv2
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk, Image

# Import the Python functions
import OS_function
import camera_function

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
            placeholder_text="Maximum number of seconds", font=("Helvetica", 14))
        
        # Modify the appearance of the entry
        self.duration_max.bind("<KeyRelease>", lambda event: self.format_numeric_max(self.frame, \
            self.duration_max.get(), initial_color))

        # Set up the position of the entry widget
        self.duration_max.grid(row=3, column=0, columnspan=4, padx=15, pady=10, sticky="ew")

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
            font=("Helvetica", 14), command=lambda: self.open_folder(self.frame))
        # Set up the position of the button widget
        self.button_path_export.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        # Launch the function that handles the image display
        self.display_image(self.frame)

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
            self.button_execute = ctk.CTkButton(master=self.frame, text="Launch", font=("Helvetica", 14), command=self.login)
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
    
    def login(self):
        pass
    #    if folder_path is defined, name projecxt, duration -> execute:
    # Ask the user to enter a int() for the duration

# Execute the GUI
def main():
    app = HydroSensApp()
    app.mainloop()

if __name__ == "__main__":
    main()
