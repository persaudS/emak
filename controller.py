import logging
import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/opt/homebrew/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg"
import tkinter
from model.model import Patient, Node
from shutdownPi import shutdownSys
from devices import BPCuff, PulseOx, Glucometer
from view import MainView
from view_dummy import MainView as MainViewDummy
import devices
from glucometerutils import glucometer

# TODO: add observer pattern for devices


class Controller:
    """Controller class for connecting Model, View, and Devices"""

    def __init__(self, dummy=False):
        if not dummy:
            self.view = MainView(self)
            # self.view.add_observer(self)
        else:
            self.view = MainViewDummy("Start")
            self.view.add_observer(self)
        self.patient = Patient()
        self._observers = []
        self.logger = self.set_logger()
        self.devices = []
        self.devices.append(BPCuff())
        self.devices.append(PulseOx())
        self.devices.append(Glucometer())

        for device in self.devices:
            device.add_observer(self)

        self.patient.add_observer(self)  # Controller is an observer of Patient
        self.add_observer(self.view)  # View is an observer of Controller
        self.add_observer(self.patient)  # Patient is an observer of Controller
        self.logger.info("Starting GUI")
        self.view_start()

    def set_logger(self):
        logging.basicConfig(filename="EMAK.log",
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        current_logger = logging.getLogger('EMAK')
        return current_logger

    # adds observer to list of observers
    def add_observer(self, observer):
        self._observers.append(observer)

    def update_state(self, main_choice, sub_choice):
        """Updates the state of the patient"""
        if main_choice == "back":
            self.patient.go_back()
            if self.patient.current_node.node_id == "Start":
                self.view.destroy()
                self.view = MainViewDummy("Start")
                self.view.add_observer(self)
                self.view_start()
                return
            self.view.update_frame(self.patient.current_node.node_id)
        else:
            if main_choice == "quick_access":
                self.patient.current_node = Node("PreQuickAccess", self.patient.model_data)
                self.patient.past_nodes.append(Node(sub_choice, self.patient.model_data))
            
            if self.patient.current_node.node_id == "EMSArrived" and main_choice == "continue":
                self._turn_off_system()
                return
            
            if main_choice == "end":
                self.patient.decide(-1)
            else:
                self.patient.decide(sub_choice)
            self.logger.info("Patient state updated")
            self.logger.info(self.patient.current_node.node_id)
            if self.patient.current_node.node_id == "BPCuff":
                self.turn_on_device("BPCuff")
            if self.patient.current_node.node_id == "PulseOx":
                self.turn_on_device("PulseOx")
            if self.patient.current_node.node_id == "Glucometer":
                self.turn_on_device("Glucometer")

            self.view.update_frame(self.patient.current_node.node_id)
            self.view.update_metrics(self.devices)
            self.logger.info("sensor frame: " + str(self.view.sensorFrame.devices[0]))
            # self.view.update_metrics(self.devices)

    #Turn off EMAK System
    def _turn_off_system(self):
        shutdownSys()

    #Turn on devices when they need to be turned on
    def turn_on_device(self, device):
        if len(self.devices) > 0:
            if (device == "BPCuff"):
                bp_device = self.devices[0]
                bp_device.turn_on()
                #self.device_notify() TODO: Figure out why this isnt working
            if (device == "PulseOx"):
                pulse_ox_device = self.devices[1]
                pulse_ox_device.turn_on()
                #self.device_notify()
            if (device == "Glucometer"):
                glucometer_device = self.devices[2]
                glucometer_device.turn_on()
                #TODO: this device does not need to be turned on
                #self.device_notify()
                if(not glucometer.device_connected()):
                     print("Connect Glucometer")
    
    #Update the patient with the retrieved device metrics 
    def patient_update(self):
        self.patient.update_metrics(self.devices)


    def device_notify(self):
        print("here", self._observers)
        for observer in self._observers:
            observer.update_metrics(self.devices)
        
        logging.info("Device status updated")

    def view_start(self):
        """Starts the view"""
        # states = {}
        # for device in self.devices:
        #     states[device.name] = device.GetStatus()
        self.logger.info("Adding device status to view")
        self.logger.info("Resize Factor: " + str(self.view.resizeFactor))
        self.view.update_metrics(self.devices)
        self.view.start()

    def base_button_click(self, text):
        return
        
    def next(self, choice):  # TODO
        # decide next node
        self.patient.decide(choice)

        # display current node
        #self.view.get_view_node(self.patient.current_node.node_id)


if __name__ == "__main__":
    controller = Controller(True)
