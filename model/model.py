import os
import json
from shutdownPi import shutdownSys


class Node:
    """Node class for the decision tree"""

    def __init__(self, node_id, model_data):
        self.node_id = node_id
        self.thresholds = []
        self.next_nodes = []
        self.device_status = []
        self.load_node(model_data)

    # loads node data from passed model data from Patient
    def load_node(self, model_data):
        """loads node data from json file"""
        node = model_data[str(self.node_id)]
        self.next_nodes = node["nextNodes"]
        self.thresholds = sorted(node["thresholds"])
        self.device_status = node["device_status"]
        return node

class Patient:
    """Patient class for navigating the decision tree"""

    def __init__(self):
       self.data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, "data/data.json"))
       self.model_data = self._load_data()
       self.current_node = Node("Start", model_data=self.model_data)
       self.past_nodes = [] # list of nodes
       self.age = None
       self.biometrics = {} # dictionary of biometrics, prob could make a class for this
       self._observers = []
    
    # loads data from json file
    def _load_data(self):
        """loads data from json file"""
        with open(self.data_path, 'r') as json_file:
            model_data = json.load(json_file).get("Nodes", {})
            return model_data
        
    # notifies observers of change
    def _notify(self):
        """""notifies observers of change"""""
        for observer in self._observers:
            observer.update(self)

    # goes back to the last node visited
    def go_back(self):
        """""goes back to the last node visited"""""
        if self.past_nodes:
            self.current_node = self.past_nodes.pop()

    # goes forward to the node with the given index in the nextNodes array
    def _go_forward(self, node_id):
        """""goes forward to the node with the given index in the nextNodes array"""""
        # If we know next node is last node, can't have its last node be this node
        self.past_nodes.append(self.current_node)
        self.current_node = Node(node_id, self.model_data)

    # decides which node is next based on the input
    def decide(self, choice):
        """""decides which node to go to based on the input"""""
        if (self.current_node.node_id == "Start"):
            self._go_forward(self.current_node.next_nodes[0])
            return
        if (self.current_node.node_id == "PreEMSArrived"):
            self._go_forward(self.current_node.next_nodes[0])
        if (self.current_node.node_id == "PreQuickAccess"):
            self._go_forward(self.current_node.next_nodes[0])
            self.past_nodes.pop()
            return
        if (self.current_node.device_status[0] == "Needed" and self.current_node.device_status[1] != "Shutdown"): 
            #Assuming controller is only observer of patient
            self._observers[0].turn_on_device(self.current_node.device_status[1])
            #Once device is turned on, we need to update biometrics with return values
            self.ptUpdate()
        
        #This is for when we need to make informed decisions automatically using the device values
        if (self.current_node.device_status[0] == "Needed"): 
            #For when the value we receive is larger than the largest value in threshold 
            #Need to figure out comparators for device specific data:
            #TODO: BPCuff: Compare Systolic and Diastolic to Threshold Sys/Dia
            #TODO: PulseOx Compare HR and OXygen to Threshold HR O2
            #TODO: Glucometer compare Glucose to Threshold Glucose
            deviceName = self.current_node.device_status[1]
            if deviceName == "BPCuff":
                data = self.biometrics.get("Blood Pressure Cuff")
                if (data is not None):
                    if (data[0] > max(self.current_node.thresholds)):
                        self._go_forward(self.current_node.next_nodes[len(self.current_node.thresholds) - 1])
                    i = 0
                    #In data.json we need to have the nextNodes organized in the same manner as threshold values 
                    for option in self.current_node.thresholds:
                        if data[0] <= option: 
                            self._go_forward(self.current_node.next_nodes[i])
                            print(i)
                            return
                        i += 1
            elif deviceName == "PulseOx":
                data = self.biometrics.get("Pulse Oximeter")
                if (data is not None):
                    if (self.biometrics.get(self.current_node.device_status[1]) > max(self.current_node.thresholds)):
                        self._go_forward(self.current_node.next_nodes[len(self.current_node.thresholds) - 1])
                    i = 0
                    #In data.json we need to have the nextNodes organized in the same manner as threshold values 
                    for option in self.current_node.thresholds:
                        if self.biometrics.get(self.current_node.device_status[1]) <= option: 
                            self._go_forward(self.current_node.next_nodes[i])
                            print(i)
                            return
                        i += 1
            elif deviceName == "Glucometer":
                data = self.biometrics.get("Glucometer")
                if (data is not None):
                    if (self.biometrics.get(self.current_node.device_status[1]) > max(self.current_node.thresholds)):
                        self._go_forward(self.current_node.next_nodes[len(self.current_node.thresholds) - 1])
                    i = 0
                    #In data.json we need to have the nextNodes organized in the same manner as threshold values 
                    for option in self.current_node.thresholds:
                        if self.biometrics.get(self.current_node.device_status[1]) <= option: 
                            self._go_forward(self.current_node.next_nodes[i])
                            print(i)
                            return
                        i += 1
            else:
                shutdownSys()
            # if (self.biometrics.get(self.current_node.device_status[1]) > max(self.current_node.thresholds)):
            #     self._go_forward(self.current_node.next_nodes[len(self.current_node.thresholds) - 1])
            # i = 0
            # #In data.json we need to have the nextNodes organized in the same manner as threshold values 
            # for option in self.current_node.thresholds:
            #     if self.biometrics.get(self.current_node.device_status[1]) <= option: 
            #         self._go_forward(self.current_node.next_nodes[i])
            #         print(i)
            #         return
            #     i += 1
        else:
            i = 0
            for option in self.current_node.thresholds:
                if choice <= option:
                    self._go_forward(self.current_node.next_nodes[i])
                    return
                i += 1
    
    # adds observer to list of observers
    def add_observer(self, observer):
        self._observers.append(observer)
    
    # Notifies observers of change
    def ptUpdate(self):
        for observer in self._observers:
            observer.patient_update()
    
    #Updates dictionary based on the device name and their values
    def update_metrics(self, devices):
        """Updates the model with new device biometrics"""
        for device in devices:
            print(self.biometrics)
            self.biometrics.update({device.name: device.value}) #Pulse is provided by both PulseOx and BPCuff, make sure to decide which one to use


# p = Patient()
# print(p.current_node.node_id)
# p.decide(0)
# print(p.current_node.node_id)

