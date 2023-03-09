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
from kivy.uix.textinput import TextInput

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        # Set columns
        self.cols = 1

        # Set a second Gridlayout
        self.top_grid = GridLayout()
        self.top_grid.cols = 2

        self.top_grid.add_widget(Label(text="Name of the sample: ")) #)), size_hint_x=None, width=500))
        self.top_grid.add_widget(Label(text="John Doe"))
        self.top_grid.add_widget(Label(text="Desired time between 2 pictures in seconds: "))
        self.delta_T = TextInput(multiline=True)
        self.top_grid.add_widget(self.delta_T)

        # Add the new top_grid to our app
        self.add_widget(self.top_grid)

        # Add a button
        self.add_widget(Button(text="Submit", on_press=self.submit_button_pressed, font_size=30, background_color=(3, 2, 4, 1)))



    def submit_button_pressed(self, button):
        print("Submit button pressed!")
 

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()