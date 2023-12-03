# from model import DecisionTree
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkmacosx import Button
import os
import json
from PIL import ImageTk, Image

from devices import DeviceState


class MainView(tk.Tk):
    """MainView class for the GUI"""

    PAD = 10

    def __init__(self, nodeTitles=["Start"]):
        super().__init__()
        self.data_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/display.json"))
        self.image_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/resources/main_frame1.jpg"))
        self._make_main_frame()

        self.resizable(False, False)
        # generate frames
        self.nodeFrames = []
        for nodeTitle in nodeTitles:
            self.nodeFrames.append(
                NodeView(self, self._get_view_node(nodeTitle), self))
        self.devices = {}

    def start(self):
        self.mainloop()

    def _make_main_frame(self):
        self.img = ImageTk.PhotoImage(
            Image.open(self.image_path).resize((777, 678)))
        self.geometry("777x678")
        self.label = tk.Label(self, image=self.img, width=777, height=678)
        # self.main_frame = ttk.Frame(self.label, width=2331, height=2034, border=0, borderwidth=0)

        self.buttom_frame = ttk.Frame(self.label)

        # Place the main frame in the grid to cover the entire screen
        self.label.place(width=777, height=678)
        self.grid_rowconfigure(0, weight=1, uniform="row", minsize=44)
        self.grid_rowconfigure(1, weight=1, uniform="row", minsize=525)
        self.grid_rowconfigure(2, weight=1, uniform="row", minsize=80, pad=5)
        self.grid_rowconfigure(3, weight=1, uniform="row")
        self.grid_columnconfigure(0, weight=1, uniform="column", minsize=10)
        self.grid_columnconfigure(1, weight=2, uniform="column", minsize=155)
        self.grid_columnconfigure(2, weight=1, uniform="column", minsize=190)
        self.grid_columnconfigure(3, weight=1, uniform="column", minsize=199)
        self.grid_columnconfigure(4, weight=1, uniform="column", minsize=199)
        self.grid_columnconfigure(5, weight=1, uniform="column")

        # self.buttom_frame = ttk.Frame(self)
        # self.buttom_frame.grid(row=0, column=0, sticky="se")

        self.continueButton = Button(
            self, text="Continue", command=lambda: self.on_state_change("continue"),
            state="disabled", bg="black", fg="white",
            font=font.Font(family='Helvetica', size=25,
                           weight='normal', slant='roman'))
        self.continueButton.grid(row=2, column=4, sticky="nsew")

        self.backButton = Button(
            self, text="Back", command=lambda: self.on_state_change("back"),
            bg="black", fg="white",
            font=font.Font(family='Helvetica', size=25,
                           weight='normal', slant='roman'))
        self.backButton.grid(row=2, column=2, sticky="nsew")

        self.endButton = Button(
            self, text="EMS Arrived", command=lambda: self.on_state_change("end"),
            bg="black", fg="white",
            font=font.Font(family='Helvetica', size=25,
                           weight='normal', slant='roman'))
        self.endButton.grid(row=2, column=3, sticky="nsew")

    def on_state_change(self, text):
        """Button submission event"""
        if text == "continue":
            print("continue")
        if text == "back":
            print("back")
        if text == "end":
            print("end")
            self.popup_window()
        pass

    def update_selected(self):
        """Updates the continue button if all selections made"""
        nodes = list(
            filter(lambda node: node.selected is not None, self.nodeFrames))
        if len(self.nodeFrames) == len(nodes) and self.continueButton is not None:
            self.continueButton['state'] = 'normal'

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
        self.sensorFrame = SensorView(self, self.devices)

    def update_frame(self, nodeTitle):
        return

    def popup_window(self):
        window = tk.Toplevel()
        window.title("EMS Arrived: Biometrics Available")
        win_x = self.winfo_rootx() + 160
        win_y = self.winfo_rooty() + 40
        window.geometry(f'+{win_x}+{win_y}')
        window.minsize(width=600, height=530)
        label = tk.Label(window, text="Hello View")
        label.pack(fill='x', padx=50, pady=5)
        button_close = tk.Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')


class NodeView():
    def __init__(self, root, node, main_view):
        self.text = node["text"]
        self.buttons = node["buttons"]
        self.selected = None
        self.main_view = main_view

        self.frame = tk.Frame(root, bg="white", width=500,
                              height=100, padx=3, pady=3)
        ttk.Label(self.frame, text=self.text, font=font.Font(family='Helvetica', size=30,
                                                             weight='bold', slant='roman'),
                  wraplength=554, justify="center", relief="solid", padding=10).pack()
        self.frame.grid(row=1, column=2, columnspan=3, sticky="nsew")
        self._make_buttons()

    # def _make_text(self):
    #     """Creates prompt text for the node"""
    #     text_frame = ttk.Frame(self.frame)
    #     ttk.Label(text_frame, text=self.text).pack()
    #     text_frame.grid(row=1, col=1, sticky="nsew")

    def _make_buttons(self):
        print("here")
        """Creates option buttons for the node"""
        for button in self.buttons:
            Button(self.frame,
                   text=button[0], width=554, command=lambda: self.button_onclick(button),
                   font=font.Font(family='Helvetica', size=25,
                                  weight='normal', slant='roman'),
                   bg="black", fg=button[1], borderless=1, pady=15).pack()
        self.frame.grid(row=1, column=2, columnspan=3, sticky="n")

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
        self.frame = tk.Frame(root, bg="#c4c4c4", width=160,
                              height=151, padx=0, pady=0)
        # ttk.Label(self.frame, text=self.text, font=font.Font(family='Helvetica', size=30,
        #                                                      weight='bold', slant='roman'),
        #           wraplength=554, justify="center", relief="solid", padding=10).pack()
        self.frame.grid(row=1, column=1, rowspan=2, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1, uniform="row", minsize=15)
        self.frame.grid_rowconfigure(1, weight=1, uniform="row", minsize=45)
        self.frame.grid_rowconfigure(2, weight=1, uniform="row", minsize=100)
        self.frame.grid_rowconfigure(3, weight=1, uniform="row", minsize=15)
        self.frame.grid_rowconfigure(4, weight=1, uniform="row", minsize=45)
        self.frame.grid_rowconfigure(5, weight=1, uniform="row", minsize=100)
        self.frame.grid_rowconfigure(6, weight=1, uniform="row", minsize=15)
        self.frame.grid_rowconfigure(7, weight=1, uniform="row", minsize=45)
        self.frame.grid_rowconfigure(8, weight=1, uniform="row", minsize=100)
        self.frame.grid_rowconfigure(9, weight=1, uniform="row", minsize=15)
        self.frame.grid_columnconfigure(0, weight=1, uniform="column", minsize=3)
        self.frame.grid_columnconfigure(1, weight=2, uniform="column", minsize=146)
        self.frame.grid_columnconfigure(2, weight=1, uniform="column", minsize=6)
        self.devices = devices
        i = 1
        for device in devices:
            labels = self.handle_text(root, device)
            labels[0].grid(row=i, column=1, sticky="sew")
            labels[1].grid(row=i+1, column=1, sticky="nsew")
            i+=3


    def handle_text(self, root, device):
        """Handles the text for the device"""
        textLabel = f"\n\n\n{device.name}:\n"

        labelStatus = None
        if device.status == DeviceState.off:
            text = f"Device Off"
            color = "yellow"
            labelStatus = tk.Label(self.frame, text=text, bg="black", fg=color, font=font.Font(family='Helvetica', size=12,
                                                             weight='normal', slant='roman'))
            
        elif device.status == DeviceState.error:
            text = f"{device.name}:\n\nDevice Error"
            color = "red"
            labelStatus = tk.Label(self.frame, text=text, bg="black", fg=color, font=font.Font(family='Helvetica', size=12,
                                                             weight='normal', slant='roman'))
        else :
            color = "green" # Add checks for vitals
            if device.name == "Blood Pressure Cuff":
                text = f"\n\n\n{device.name}\n\nSystolic: {device.value['systolic']}\nDiastolic: {device.value['diastolic']}\nPulse: {device.value['pulse']}"
            elif device.name == "Pulse Oximeter":
                text = f"{device.name}\n\nPulse: {device.value['pulse']}\nOxygen: {device.value['oxygen']}"
            elif device.name == "Glucometer":
                text = f"{device.name}\n\nGlucose: {device.value}"
            else:
                text = f"{device.name}\n\n{device.value}"
                labelStatus = tk.Label(self.frame, text=text, bg="black", fg=color, font=font.Font(family='Helvetica', size=12,
                                                         weight='normal', slant='roman'))
                
        labelName = tk.Label(self.frame, text=textLabel, bg="black", fg=color, font=font.Font(family='Helvetica', size=13,
                                                             weight='bold', slant='roman'))
        labels = [labelName, labelStatus]
        return labels
if __name__ == "__main__":
    main = MainView(["IsSceneSafe"])
    main.start()
    # print('MVC - the simplest example')
    # print('Do you want to see everyone in my db?[y/n]')
