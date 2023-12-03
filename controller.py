import logging
import tkinter
from model.model import Patient
from devices import BPCuff, PulseOx, Glucometer
from view import MainView
from view_dummy import MainView as MainViewDummy
import devices

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
        elif main_choice == "end":
            print("End")
        else:
            self.patient.decide(sub_choice)
            self.logger.info("Patient state updated")
            self.logger.info(self.patient.current_node.node_id)
            # Update device state when the node title is "PulseOx"
            if self.patient.current_node.node_id == "BPCuff":
                self.turn_on_device("BPCuff")
            if self.patient.current_node.node_id == "PulseOx":
                self.turn_on_device("PulseOx")
            if self.patient.current_node.node_id == "Glucometer":
                self.turn_on_device("Glucometer")
            self.view.update_frame(self.patient.current_node.node_id)
    
    def turn_on_device(self, device):
        print(self.devices[1])
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
                #self.device_notify() 



    def device_notify(self):
        for observer in self._observers:
            observer.update_metrics(self.devices)
        
        logging.info("Device status updated")

    def view_start(self):
        """Starts the view"""
        # states = {}
        # for device in self.devices:
        #     states[device.name] = device.GetStatus()
        self.logger.info("Adding device status to view")
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
