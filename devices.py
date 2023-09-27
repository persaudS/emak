from enum import Enum


class DeviceState(str, Enum):
    on_no_reading = 'Online, No Reading'
    on_reading = 'Online, Reading'
    off = 'Off'
    error = 'Error'


class Device(object):
    
    """Class for abstract medical device"""

    self.status = DeviceState.off

    def __init__(self):
        self.status = DeviceState.off
    
    def GetStatus(self):
        return self.status

    def Start(self):
        return False
    
    def GetReading(self):
        return None
 
 
class BPCuff(Device):
 
    """Class for BP Cuff"""
 
    def __init__(self):
        super()
        self.name = "Blood Pressure Cuff"
        self.Start()
 
    def Start(self):
        self.status = DeviceState.on
    
    def GetReading(self):
        readings = {}
        readings['systolic'] = 120
        readings['diastolic'] = 80
        return readings
 
 
class PulseOx(Device):
 
    """Class for Pulse Ox"""
 
    def __init__(self):
        super()
        self.name = "Pulse Oximeter"
        self.Start()
 
    def Start(self):
        self.status = DeviceState.on
    
    def GetReading(self):
        readings = {}
        readings['pulse'] = 80
        readings['oxygen'] = 98
        return [120, 80]
 
 
class Glucometer(Device):
 
    """Class for Glucometer"""
 
    def __init__(self):
        super()
        self.name = "Glucometer"
        self.Start()
 
    def Start(self):
        self.status = DeviceState.on
 
