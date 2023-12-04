from enum import Enum
from glucometerutils import glucometer
from bloodPressure import getBPData


class DeviceState(str, Enum):
    on = 'online'
    off = 'off'
    error = 'error'


class Device(object):
    
    """Class for abstract medical device"""

    def __init__(self):
        self.status = DeviceState.off
        self.name = None
        self.value = None
        self._observers = []
    
    def get_status(self):
        return self.status

    def start(self):
        return False
    def add_observer(self, observer):
        self._observers.append(observer)

    def notify(self):
        for observer in self._observers:
            observer.device_notify()

 
 
class BPCuff(Device):
 
    """Class for BP Cuff"""
 
    def __init__(self):
        super().__init__()
        self.name = "Blood Pressure Cuff"
        self.value = {"systolic": None, "diastolic": None, "pulse": None}
        self.start()
 
    def Start(self):
        self.status = DeviceState.off
    
    def turn_on(self): 
        print("BPCuff")
        data = getBPData()
        self.value["systolic"] = data[0]
        self.value["diastolic"] = data[1]
        self.value["pulse"] = data[2]
        self.status = DeviceState.off
 
 
class PulseOx(Device):
 
    """Class for Pulse Ox"""
 
    def __init__(self):
        super().__init__()
        self.name = "Pulse Oximeter"
        self.value = {"pulse": None, "oxygen": None}
        self.start()
 
    def Start(self):
        self.status = DeviceState.off
    
    def turn_on(self): 
        print("PulseOx")
 
 
class Glucometer(Device):
 
    """Class for Glucometer"""
 
    def __init__(self):
        super().__init__()
        self.name = "Glucometer"
        self.value = None
        self.start()
 
    def start(self):
        self.status = DeviceState.off
    
    def turn_on(self): 
        print("Glucometer")
        print(glucometer.device_connected())
        print(glucometer.get_last())