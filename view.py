# from model import DecisionTree
import tkinter as tk
from tkinter import ttk
import os
import json
from PIL import ImageTk, Image


class MainView(tk.Tk):
    """MainView class for the GUI"""

    PAD = 10

    def __init__(self, controller, nodeTitles=["Start"]):
        super().__init__()
        self.data_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), os.pardir, "data/display.json"))
        self.image_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/resources/main_frame.png"))

        self.controller = controller
        self._make_main_frame()

        self.device_states = controller.devices.map(
            lambda device: device.get_status())

        # generate frames
        self.nodeFrames = []
        for nodeTitle in nodeTitles:
            self.nodeFrames.append(
                NodeView(self, self._get_view_node(nodeTitle), self.controller, self))

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
        self.main_frame = ttk.Frame(self)
        self.img = ImageTk.PhotoImage(Image.open(self.image_path))  # label image (frame background)
        self.label = tk.Label(self, image = self.img, width=1554, height=1356)  # frame parent
        self.main_frame = ttk.Frame(self.label, width=1554, height=1356)
        self.geometry("1554x1356")
        self.label.pack()
        self.main_frame.pack(padx=self.PAD, pady=self.PAD)

    def on_state_change(self, text):
        """Button submission event"""
        if text == "continue":
            self.controller.next(list(map(lambda node: int(node.selected), self.nodeFrames)))
        if text == "back":
            self.controller.next([0])
        if text == "end":
            self.controller.next([-1])
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
            node = view_data.get(nodeTitle, {})
            return node

    def update_metrics(self, devices):
        """Updates the view with new device states"""
        self.devices = devices

    def button_onclick(self, text):
        if text == 'Back':
            self.controller.back()
        elif text == 'Continue':
            # check if the Node views have selections
            # if yes
            self.controller.next()


class NodeView():
    def __init__(self, root, node, controller, main_view):
        self.frame = tk.Frame(root, bg="red")
        self.text = node["text"]
        self.buttons = node["buttons"]
        self.controller = controller
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
    main = MainView("Start")

    # print('MVC - the simplest example')
    # print('Do you want to see everyone in my db?[y/n]')
