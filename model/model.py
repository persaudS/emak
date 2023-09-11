
class DecisionTree:

   def __init__(self):
      self.currentNode = None
   
   def getStatus(self):
      return self.diagnosis
   
   def setNextNode(self, node):
      self.currentNode = node

   
class ActionTree(TreeNode):
   


#represents a diagnosis with:
#   - name
#   - description
#   - some sort of followup 
#        - ie "go to the ER" or "find AED"
#        - or buttons for next steps
class Diagnosis(object): #TODO
      def __init__(self):
      self.diagnosis = "Undecided"


