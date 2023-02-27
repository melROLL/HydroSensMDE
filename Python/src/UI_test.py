"""import PySimpleGUI as sg
import os.path

sg.Window(title="HydroSesMDE", layout=[[]], margins=(100, 50)).read()

# First the window layout in 2 columns


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")
    ],
]"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3 
        self.rows = 6
        self.add_widget(Label(text="Name: ", size_hint_x=None, width=100))
        self.add_widget(Label(text="John Doe"))
        self.add_widget(Label(text="Age: "))
        self.add_widget(Label(text="30"))
        # Add a button
        self.add_widget(Button(text="Submit", on_press=self.submit_button_pressed, font_size=30, background_color=(3, 2, 4, 1)))

    def submit_button_pressed(self, button):
        print("Submit button pressed!")
 

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()