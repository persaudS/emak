import logging
import tkinter
from model.model import Patient
from devices import BPCuff, PulseOx, Glucometer
from view import MainView
import devices

# TODO: add observer pattern for devices


class Controller:
    """Controller class for connecting Model, View, and Devices"""

    def __init__(self):
        self.view = MainView(self)
        self.patient = Patient()
        self.patient.add_observer(self)  # Controller is an observer of Patient
        self.add_observer(self.view)  # View is an observer of Controller
        self.add_observer(self.patient)  # Patient is an observer of Controller
        self.logger = self.set_logger()
        self.logger.info("Starting GUI")
        self.devices = []
        self.devices.append(BPCuff())
        self.devices.append(PulseOx())
        self.devices.append(Glucometer())
        self._observers = []
        self.view_start()

    def set_logger(self):
        logging.basicConfig(filename="EMAK.log",
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

        current_logger = logging.getLogger('EMAK')
        return current_logger

    # adds observer to list of observers
    def add_observer(self, observer):
        self._observers.append(observer)

    def device_notify(self):
        for observer in self._observers:
            observer.update_metrics(self.devices)

    def view_start(self):
        """Starts the view"""
        states = {}
        for device in self.devices:
            states[device.name] = device.GetStatus()
        self.logger.info("Adding device status to view")
        self.view.set_states(states)

        self.view.start()

    def next(self):  # TODO
        choice = self.view.patientInput()
        # decide next node
        self.patient.decide(choice)

        # display current node
        self.view.get_view_node(patient.current_node.node_id)


if __name__ == "__main__":
    # running controller function
    c = Controller()
