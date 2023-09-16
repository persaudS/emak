import os
import json


class Node:
    """Node class for the decision tree"""

    def __init__(self, node_id):
        self.node_id = node_id
        self.data_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, "/data/data.json")) #TODO: change this to the correct path
        print(self.data_path)
        self.thresholds = []
        node_id = ""
        self.next_nodes = []
        self.load_data()

    # loads node data from json file
    def load_data(self):
        """loads node data from json file"""
        node_data = json.loads(self.data_path).get("Nodes", {})
        node = node_data[str(self.node_id)]
        self.next_nodes = node["nextNodes"]
        self.thresholds = sorted(node["thresholds"])
        return node

class Patient:
    """Patient class for navigating the decision tree"""
    def __init__(self):
       self.current_node = Node("Start")   
       self.past_nodes = [] # list of nodes
       self.age = None
       self.blood_pressure = None
       self.pulse_ox = None
       self.glucose = None
       self.current_node = None
    
    # goes back to the last node visited
    def go_back(self):
        """""goes back to the last node visited"""""
        if self.past_nodes:
            self.current_node = self.past_nodes.pop()

    # goes forward to the node with the given index in the nextNodes array
    def go_forward(self, node_id):
        """""goes forward to the node with the given index in the nextNodes array"""""
        # If we know next node is last node, can't have its last node be this node
        self.past_nodes.append(self.current_node)
        self.current_node = Node(node_id)

    # decides which node is next based on the input
    def decide(self, choice):
        """""decides which node to go to based on the input"""""
        i = 0
        for option in self.current_node.thresholds:
            if choice <= option:
                self.go_forward(self.current_node.next_nodes[i])
            i += 1


p = Patient()
print(p.current_node.id)
p.decide(0)
print(p.current_node.id)

