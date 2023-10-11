# from model import DecisionTree
import tkinter as tk
from tkinter import ttk
import os
import json
from PIL import ImageTk, Image


class MainView(tk.Tk):
    """MainView class for the GUI"""

    PAD = 10

    def __init__(self, nodeTitles=["Start"]):
        super().__init__()
        self.data_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/display.json"))
        self.image_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/resources/main_frame.png"))
       
        self._make_main_frame()

        # generate frames
        self.nodeFrames = []
        for nodeTitle in nodeTitles:
            self.nodeFrames.append(
                NodeView(self, self._get_view_node(nodeTitle), self))
        self.device_states = {}
        self.sensorFrame = SensorView(self, self.device_states)

        self.continueButton = ttk.Button(
            self, text="Continue", command=lambda: self.on_state_change("continue"), state="disabled").pack(side="bottom")
        self.backButton = ttk.Button(
            self, text="Back", command=lambda: self.on_state_change("back")).pack(side="bottom")
        self.endButton = ttk.Button(
            self, text="EMS Arrived", command=lambda: self.on_state_change("end")).pack(side="bottom")

    def start(self):
        self.mainloop()

    def _make_main_frame(self):
        
        self.img = ImageTk.PhotoImage(Image.open(self.image_path))  # label image (frame background)
        self.label = tk.Label(self, image = self.img, width=1554, height=1356)  # frame parent
        self.main_frame = ttk.Frame(self.label, width=1554, height=1356)
        self.geometry("1554x1356")
        self.main_frame.pack(padx=self.PAD, pady=self.PAD)
        self.label.pack()

    def on_state_change(self, text):
        """Button submission event"""
        if text == "continue":
            print("continue")
        if text == "back":
            print("back")
        if text == "end":
            print("end")
        pass

    def update_selected(self):
        """Updates the continue button if all selections made"""
        nodes = list(filter(lambda node: node.selected is not None, self.nodeFrames))
        if len(self.nodeFrames) == len(nodes) and self.continueButton is not None:
            self.continueButton.config(state="normal")


    def set_states(self, states):
        """Sets the states of the devices"""
        self.device_states = states
        # TODO: update view with new states
        return None

    def _get_view_node(self, nodeTitle):
        """Gets the node view information from json file"""
        with open(self.data_path, 'r') as json_file:
            view_data = json.load(json_file).get("Nodes", {})
            node = view_data[nodeTitle]
            return node

    def update_metrics(self, devices):
        """Updates the view with new device states"""
        self.devices = devices


class NodeView():
    def __init__(self, root, node, main_view):
        self.frame = tk.Frame(root, bg="red")
        self.text = node["text"]
        self.buttons = node["buttons"]
        self.selected = None
        self.main_view = main_view

        self._make_text()
        self._make_buttons()

    def _make_text(self):
        """Creates prompt text for the node"""
        text_frame = ttk.Frame(self.frame)
        text_frame.pack()

        ttk.Label(text_frame, text=self.text).pack()

    def _make_buttons(self):
        """Creates option buttons for the node"""

        for button in self.buttons:
            ttk.Button(self.frame,
                       text=button, command=lambda: self.button_onclick(button)).pack()

    def button_onclick(self, button):
        """Button click event"""
        i = None
        for i in range(len(self.buttons)):
            if self.buttons[i] == button:
                break
        self.selected = i
        self.main_view.update_selected()
        return


class SensorView(tk.Frame):
    def __init__(self, root, devices):
        tk.Frame(root, bg="white")
        self.devices = devices

    def update_metrics(self, devices):
        """Updates the view with new device states"""
        self.devices = devices


if __name__ == "__main__":
    main = MainView(["Start"])
    main.start()
    # print('MVC - the simplest example')
    # print('Do you want to see everyone in my db?[y/n]')
