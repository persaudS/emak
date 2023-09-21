import logging
from model import Patient
from devices import BPCuff, PulseOx, Glucometer
import view
import devices


class Controller:
   """Controller class for connecting Model, View, and Devices"""

   def __init__(self):
      self.patient = Patient()
      self.view = View()
      self.devices = []
      self.devices.append(BPCuff())
      self.devices.append(PulseOx())
      self.devices.append(Glucometer())
      self.logger = self._set_logger()
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
      logger.info("Starting GUI")
      self.view.start(states)

   def next():
      # get input
      choice = view.patientInput()
      # decide next node
      patient.decide(choice)

      # display current node
      view.display_node(patient.current_node)


if __name__ == "__main__":
   # running controller function
   patient = Patient()
   start()
