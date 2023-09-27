import os
import json


class Node:
    """Node class for the decision tree"""

    def __init__(self, node_id, model_data):
        self.node_id = node_id
        self.thresholds = []
        self.next_nodes = []
        self.load_node(model_data)

    # loads node data from passed model data from Patient
    def load_node(self, model_data):
        """loads node data from json file"""
        node = model_data[str(self.node_id)]
        self.next_nodes = node["nextNodes"]
        self.thresholds = sorted(node["thresholds"])
        return node

class Patient:
    """Patient class for navigating the decision tree"""
    def __init__(self):
       self.data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, "data/data.json"))
       self.model_data = self._load_data()
       self.current_node = Node("Start", model_data=self.model_data)   
       self.past_nodes = [] # list of nodes
       self.age = None
       self.blood_pressure = None
       self.pulse_ox = None
       self.glucose = None
       self._observers = []
    
    # adds observer to list of observers
    def add_observer(self, observer):
        """""adds observer to list of observers"""""
        if(observer in self._observers):
            return
        self._observers.append(observer)

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
    def _go_back(self):
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
        i = 0
        for option in self.current_node.thresholds:
            if choice <= option:
                self._go_forward(self.current_node.next_nodes[i])
            i += 1
        self._notify()
    



p = Patient()
print(p.current_node.node_id)
p.decide(0)
print(p.current_node.node_id)

