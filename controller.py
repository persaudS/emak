import logging
import tkinter
from model.model import Patient
from devices import BPCuff, PulseOx, Glucometer
from view import View
import devices


class Controller:
   """Controller class for connecting Model, View, and Devices"""

   def __init__(self):
      self.logger = self._set_logger()
      self.patient = Patient()
      self.patient.add_observer(self)
      self.logger.info("Starting GUI")
      self.view = View(tkinter.Tk(), self.patient) 
      self.view.add_observer(self)
      self.devices = []
      self.devices.append(BPCuff())
      self.devices.append(PulseOx())
      self.devices.append(Glucometer())
      self.get_device_status()

   def _set_logger(self):
       logging.basicConfig(filename="EMAK.log",
                           filemode='a',
                           format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                           datefmt='%H:%M:%S',
                           level=logging.DEBUG)

       current_logger = logging.getLogger('EMAK')
       return current_logger

   def device_notify(self):
      """Starts the view"""
      states = {}
      self.logger.info("Getting devices' statuses.")
      for device in self.devices:
         status = device.GetStatus()
         states[device.name] = status
         if status == "Error":
            self.logger.warning(device.name + ": " + status)
         if status == "Online, Reading:":
            self.logger.info(device.name + ": " + status + "\nData: " + str(device.GetData()))
            self.patient.new_reading(device.name, device.GetData())
            self.view.new_reading(device.name, device.GetData())

      self.view.update_devices(states)

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
