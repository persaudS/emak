import logging
import tkinter
from model.model import Patient
from devices import BPCuff, PulseOx, Glucometer
from view import StartView
import devices


class Controller:
   """Controller class for connecting Model, View, and Devices"""

   def __init__(self):
      self.logger = self._set_logger()
      self.patient = Patient()
      self.logger.info("Starting GUI")
      self.view = StartView(tkinter.Tk())
      self.devices = []
      self.devices.append(BPCuff())
      self.devices.append(PulseOx())
      self.devices.append(Glucometer())
      self._view_start()

   def _set_logger(self):
       logging.basicConfig(filename="EMAK.log",
                           filemode='a',
                           format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                           datefmt='%H:%M:%S',
                           level=logging.DEBUG)

       current_logger = logging.getLogger('EMAK')
       return current_logger

   def _view_start(self):
      """Starts the view"""
      states = {}
      for device in self.devices:
         states[device.name] = device.GetStatus()
      self.logger.info("Adding device status to view")
      self.view.set_states(states)

   def next(self):
      # get input
      choice = self.view.patientInput()
      # decide next node
      patient.decide(choice)

      # display current node
      view.get_view_node(patient.current_node.node_id)


if __name__ == "__main__":
   # running controller function
   patient = Patient()
   start()
