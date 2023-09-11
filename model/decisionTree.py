class DecisionTree():

    currentNode = None
    def __init__(self):
        self.currentNode = None #would make this the first node of the tree
        
    #move to the next node based on priority (if breathing stops or blood pressure drops the decision tree state doesn't matter)    
    def moveNext(self, value):
        self.currentNode.getNextTreeNode(value)
    