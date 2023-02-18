import cv2
import tkinter as tk

class WebcamCaptureApp:

    def __init__(self):
        # create the main window
        self.root = tk.Tk()
        self.root.title("Webcam Capture")

        # create the capture button
        self.capture_button = tk.Button(self.root, text="Capture", command=self.capture)
        self.capture_button.pack(pady=10)

        # create the quit button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

        # initialize the camera
        self.cap = cv2.VideoCapture(0)

    def capture(self):
        # capture a frame
        ret, frame = self.cap.read()

        # save the captured image to a file
        cv2.imwrite("image.jpg", frame)

    def quit(self):
        # release the camera and close the window
        self.cap.release()
        self.root.destroy()

    def run(self):
        # start the main loop
        self.root.mainloop()

# create the app object and run it
app = WebcamCaptureApp()
app.run()
