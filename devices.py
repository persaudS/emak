from enum import Enum


class DeviceState(str, Enum):
    on = 'online'
    off = 'off'
    error = 'error'


class Device(object):
    
    """Class for abstract medical device"""

    self.status = DeviceState.off

    def __init__(self):
        self.status = DeviceState.off
    
    def GetStatus(self):
        return self.status

    def Start(self):
        return False
 
 
class BPCuff(Device):
 
    """Class for BP Cuff"""
 
    def __init__(self):
        super()
        self.name = "Blood Pressure Cuff"
        self.Start()
 
    def Start(self):
        self.status = DeviceState.on
 
 
class PulseOx(Device):
 
    """Class for Pulse Ox"""
 
    def __init__(self):
        super()
        self.name = "Pulse Oximeter"
        self.Start()
 
    def Start(self):
        self.status = DeviceState.on
 
 
class Glucometer(Device):
 
    """Class for Glucometer"""
 
    def __init__(self):
        super()
        self.name = "Glucometer"
        self.Start()
 
    def Start(self):
        self.status = DeviceState.on
 
