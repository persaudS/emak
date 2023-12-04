# from model import DecisionTree
import math
import threading
import tkinter as tk
import pygame
from tkinter import ttk
from tkinter import font
from tkmacosx import Button
import tkvideo as tkv
import os
import json
from PIL import ImageTk, Image

from devices import DeviceState


class MainView(tk.Tk):
    """MainView class for the GUI"""

    PAD = 10

    def __init__(self, nodeTitle="Start"):
        super().__init__()
        self._observers = []
        self.data_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/display.json"))
        self.image_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/resources/main_frame3.jpg"))
        self._make_main_frame(nodeTitle)
        # self.attributes('-fullscreen', True)
        self.wm_attributes('-fullscreen', 1)
        self.resizable(True, True)
        self.state('zoomed')
        # generate frames
        self.devices = {}
        self.nodeFrame = NodeView(self, self._get_view_node(nodeTitle), self, nodeTitle)
        self.nodeFrame.add_observer(self)





    def start(self):
        self.mainloop()

    def update_frame(self, nodeTitle):
        """Updates the node frame"""
        if nodeTitle == "IsSceneSafe":
            self.sensorFrame = SensorView(self, self.devices)
            self.continueButton.destroy()
            self.backButton.destroy()
            self.toggle_button.destroy()
            self.continueButton = Button(
                self, text="Continue", command=lambda: self.on_state_change("continue", None),
                state="disabled", bg="black", fg="white", 
                font=font.Font(family='Helvetica', size=25,
                            weight='normal', slant='roman'))
            self.continueButton.grid(row=2, column=4, sticky="nsew")

            self.backButton = Button(
                self, text="Back", command=lambda: self.on_state_change("back", None),
                bg="black", fg="white",
                font=font.Font(family='Helvetica', size=25,
                            weight='normal', slant='roman'))
            self.backButton.grid(row=2, column=2, sticky="nsew")

            self.endButton = Button(
                self, text="EMS Arrived", command=lambda: self.on_state_change("end", None),
                bg="black", fg="white",
                font=font.Font(family='Helvetica', size=25,
                            weight='normal', slant='roman'))
            self.endButton.grid(row=2, column=3, sticky="nsew")
            
            self.toggle_button = Button(
                self, text="Quick Access", command=lambda: self.quick_access_popup_window(),
                bg="black", fg="white",
                font=font.Font(family='Helvetica', size=15, weight='normal', slant='roman'))
            self.toggle_button.grid(row=2, column=1, sticky="nsew")
        elif nodeTitle == "Start":
            self.sensorFrame.frame.destroy()
        else:
            self.continueButton['state'] = 'disabled'
        self.nodeFrame.frame.destroy()
        self.nodeFrame = NodeView(self, self._get_view_node(nodeTitle), self, nodeTitle)
        self.nodeFrame.add_observer(self)

    # def resize(event):
    #     print("New size is: {}x{}".format(event.width, event.height))



    def _make_main_frame(self, nodeTitle):
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        print(w," ", h)
        w = int(h * 1.80)
        self.resizeFactor = h / 777
        self.geometry("%dx%d+0+0" % (w, h))
        # self.bind("<Configure>", self.resize)
        self.overrideredirect(True)
        self.img = ImageTk.PhotoImage(
            Image.open(self.image_path).resize((w, h)))
        # self.geometry("777x678")
        self.label = tk.Label(self, image=self.img, width=w, height=h, justify="center")

        # self.main_frame = ttk.Frame(self.label, width=2331, height=2034, border=0, borderwidth=0)

        self.buttom_frame = ttk.Frame(self.label)
        self.nodeTitle = nodeTitle

        # Place the main frame in the grid to cover the entire screen
        self.label.place(width=w, height=h)
        self.grid_rowconfigure(0, weight=1, uniform="row", minsize=int(44*self.resizeFactor))
        self.grid_rowconfigure(1, weight=1, uniform="row", minsize=int(525*self.resizeFactor))
        self.grid_rowconfigure(2, weight=1, uniform="row", minsize=int(80*self.resizeFactor), pad=5)
        self.grid_rowconfigure(3, weight=1, uniform="row")
        self.grid_columnconfigure(0, weight=1, uniform="column", minsize=int(10*self.resizeFactor))
        self.grid_columnconfigure(1, weight=2, uniform="column", minsize=int(155*self.resizeFactor))
        self.grid_columnconfigure(2, weight=1, uniform="column", minsize=int(190*self.resizeFactor))
        self.grid_columnconfigure(3, weight=1, uniform="column", minsize=int(199*self.resizeFactor))
        self.grid_columnconfigure(4, weight=1, uniform="column", minsize=int(199*self.resizeFactor))
        self.grid_columnconfigure(5, weight=1, uniform="column")
        self.label.grid(row=0, columnspan=6, rowspan=4, column=0, sticky="nsew")

        if nodeTitle == "Start":
                self.labelCover = tk.Label(self, bg="white", width=int(155*self.resizeFactor), height=int(80*self.resizeFactor))
                self.labelCover.grid(row=2, rowspan=1, column=1, pady=2, sticky="nsew")  
                self.continueButton = Button(
                self, text="I'm Ready", command=lambda: self.on_state_change("continue", None),
                state="normal", bg="green", fg="black", pady=5, padx=5,
                font=font.Font(family='Helvetica', size=25, 
                            weight='normal', slant='roman'))
                self.continueButton.grid(row=2, column=3, sticky="nsew")

                self.backButton = Button(
                    self, text="Cancel", command=lambda: self.on_state_change("back", None),
                    bg="red", fg="black", pady=5, padx=5,
                    font=font.Font(family='Helvetica', size=25,
                                weight='normal', slant='roman'))
                self.backButton.grid(row=2, column=2, sticky="nsew")

        else:
            self.continueButton = Button(
                self, text="Continue", command=lambda: self.on_state_change("continue", None),
                state="disabled", bg="black", fg="white", 
                font=font.Font(family='Helvetica', size=25,
                            weight='normal', slant='roman'))
            self.continueButton.grid(row=2, column=4, sticky="nsew")

            self.backButton = Button(
                self, text="Back", command=lambda: self.on_state_change("back", None),
                bg="black", fg="white",
                font=font.Font(family='Helvetica', size=25,
                            weight='normal', slant='roman'))
            self.backButton.grid(row=2, column=2, sticky="nsew")

            self.endButton = Button(
                self, text="EMS Arrived", command=lambda: self.on_state_change("end", None),
                bg="black", fg="white",
                font=font.Font(family='Helvetica', size=25,
                            weight='normal', slant='roman'))
            self.endButton.grid(row=2, column=3, sticky="nsew")

            self.toggle_button = Button(
                self, text="Quick Access", command=lambda: self.quick_access_popup_window(),
                bg="black", fg="white",
                font=font.Font(family='Helvetica', size=15, weight='normal', slant='roman'))
            self.toggle_button.grid(row=3, column=1, sticky="nsew")

    def on_state_change(self, text, quickAccessChoice):
        """Button submission event"""
        if text == "end":
            print("end")
            self.ems_popup_window()
        elif text == "quick_access": 
            self.nodeFrame.frame.destroy()
            self.update_observers(text, quickAccessChoice)
        else:
            # if(self.nodeFrame.video):
            #     self.nodeFrame.stop_audio()
                # self.nodeFrame.mixer.music.unload()
                # self.nodeFrame.mixer.quit()
                # audioThread = threading.Thread(target=self.nodeFrame.mixer.music.pause, args=()) 
                # audioThread.start()
                
            self.nodeFrame.frame.destroy()
            self.update_observers(text, self.nodeFrame.selected)
        pass
    
    def update_observers(self, main_choice, option_choice):
        """Updates observers with new states"""
        for observer in self._observers:
            observer.update_state(main_choice, option_choice)


    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def update_selected(self):
        """Updates the continue button if all selections made"""
        if (self.nodeFrame.selected is not None):
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
        if self.nodeTitle == "Start":
            return
        self.sensorFrame = SensorView(self, self.devices)

    def ems_popup_window(self):
        window = tk.Toplevel()
        window.title("EMS Arrived: Biometrics Available")
        win_x = self.winfo_rootx() + 160
        win_y = self.winfo_rooty() + 40
        window.geometry(f'+{win_x}+{win_y}')
        window.minsize(width=600, height=530)
        label = tk.Label(window, text="Hello Dummy View")
        label.pack(fill='x', padx=50, pady=5)
        button_close = tk.Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')

    def quick_access_popup_window(self):
        window = tk.Toplevel()
        window.title("Quick Access Panel")
        win_x = self.winfo_rootx() + 160
        win_y = self.winfo_rooty() + 40
        window.geometry(f'+{win_x}+{win_y}')
        window.minsize(width=600, height=530)
        button_close = tk.Button(window, text="Close", command=window.destroy)
        button_close.pack(fill='x')
        
        # Define button titles TODO: Get images for the buttons
        button_titles = [
            ["Heart Emergency", 0],
            ["Patient Fall", 1],
            ["Bleeding", 2],
            ["Stroke", 3],
            ["Choking", 4],
            ["Unknown Medical", 5],
            ["Unknown Trauma", 6]
        ]

        for title in button_titles:
            button = self.handle_text(window, title)
            button.pack(fill='both', expand=False)

    def handle_text(self, root, title):
        """Handles the text for the quick access buttons"""
        button = tk.Button(root, text=title[0], command=lambda: self.on_state_change("quick_access", title[1]), font=font.Font(family='Helvetica', size=15, weight='normal'))
        button.config(width=15, height=3, pady=10, anchor="center")

        return button



class NodeView():
    def __init__(self, root, node, main_view, nodeTitle):
        self.resizeFactor = main_view.resizeFactor
        self.text = node["text"]
        self.buttons = node["buttons"]
        self.selected = None
        self.main_view = main_view
        self.nodeTitle = nodeTitle
        self._observers = []
        self.frame = tk.Frame(root, bg="white", width=int(500*self.resizeFactor),
                              height=int(100*self.resizeFactor), padx=3, pady=3)

        if nodeTitle == "Start":
            self.frame.grid(row=1, column=1, columnspan=4, sticky="nsew")
            ttk.Label(self.frame, text=self.text, font=font.Font(family='Helvetica', size=20,
                                                             weight='bold', slant='roman'),
                  wraplength=int(700*self.resizeFactor), justify="center", relief="solid", padding=10).pack()
        else:
            ttk.Label(self.frame, text=self.text, font=font.Font(family='Helvetica', size=25,
                                                             weight='bold', slant='roman'),
                  wraplength=int(554*self.resizeFactor), justify="center", relief="solid", padding=10).pack()
           
        
        if node.get("video", None) is not None:
            self.video = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "data/resources/", node["video"]))
            self.audio = self.video.replace("mp4", "wav")
            self._play_audio()
            self.video_label = tk.Label(self.frame, bg="black", width=int(450*self.resizeFactor), height=int(253*self.resizeFactor))
            self.video_label.pack()
            vidThread = threading.Thread(target=self._generate_video, args=()) 
            vidThread.start()
        
        self._make_buttons()


    def _generate_video(self):
        """Generates the video for the node"""
        video = tkv.tkvideo(self.video, self.video_label, loop=1, size=(int(450*self.resizeFactor),int(253*self.resizeFactor)))
        video.play()

    def _play_audio(self):
        """Plays audio for the node"""
        # pygame.init()
        self.mixer = pygame.mixer
        self.mixer.init()
        self.mixer.music.load(self.audio)
        self.mixer.music.play(loops = -1)
    
    def stop_audio(self):
        """Stops audio for the node"""
        self.mixer.music.stop()
        self.mixer.quit()


    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def _make_buttons(self):
        """Creates option buttons for the node"""
        for button in self.buttons:
            Button(self.frame,
                   text=button[0], width=int(554*self.resizeFactor), command=lambda option=button[0]: self.button_onclick(option),
                   font=font.Font(family='Helvetica', size=25,
                                  weight='normal', slant='roman'),
                   bg="black", fg=button[1], borderless=1, pady=15).pack()
        self.frame.grid(row=1, column=2, columnspan=3, sticky="n")

    def button_onclick(self, button):
        """Button click event"""
        if self.audio:
            self.stop_audio()
        i = 0
        for i in range(len(self.buttons)):
            if self.buttons[i][0] == button:
                break
        self.selected = i
        for observer in self._observers:
            observer.update_selected()
        return


class SensorView(tk.Frame):
    def __init__(self, root, devices):
        self.resizeFactor = root.resizeFactor
        self.frame = tk.Frame(root, bg="#c4c4c4", width=160,
                              height=100, borderwidth=5, relief="ridge", padx=0, pady=0)
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
    main = MainView("Start")
    main.start()
    # print('MVC - the simplest example')
    # print('Do you want to see everyone in my db?[y/n]')
