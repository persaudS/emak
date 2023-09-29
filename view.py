# from model import DecisionTree
import tkinter as tk
from tkinter import ttk
import os
import json


class MainView(tk.Tk):
    """MainView class for the GUI"""

    PAD = 10

    def __init__(self, controller, nodeTitle="Start"):
        super().__init__()
        self.data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, "data/display.json"))
        
        self.controller = controller
        
        self.title(nodeTitle)
        self._make_main_frame()
        
        self.device_states = {} #TODO: get device states from controller
        
        ## generate frames
        self.nodeFrame = NodeView(self, self._get_view_node(nodeTitle))
        self.sensorFrame = SensorView(self, self.device_states)
        

    def start(self):
        self.mainloop()
    
    def _make_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=self.PAD, pady=self.PAD)

    def on_state_change(self):
        #TODO: button was clicked
        pass
    
    def set_states(self, states):
        """Sets the states of the devices"""
        self.device_states = states
        #TODO: update view with new states
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

class NodeView(tk.Frame):
    def __init__(self, root, node):
        tk.Frame(root, bg="red")
        self.text = node["text"]
        self.buttons = node["buttons"]
        
        self._make_text()
        self._make_buttons()
        
    
    def _make_text(self):
        """Creates prompt text for the node"""
        text_frame = ttk.Frame(self)
        text_frame.pack()
        
        ttk.Label(text_frame, text=self.text).pack()
    
    def _make_buttons(self):
        """Creates option buttons for the node"""
        button_frame = ttk.Frame(self)
        button_frame.pack()
        
        for button in self.buttons:
            ttk.Button(button_frame, text=button["text"], command=button_onclick(button["text"])).pack()
    
    def button_onclick(self, text):
        """Button click event"""
        pass
    

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
