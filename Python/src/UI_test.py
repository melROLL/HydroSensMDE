import PySimpleGUI as sg
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
]