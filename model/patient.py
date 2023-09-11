#represents a patient with:
#   - name
#   - age
#   - blood pressure
#   - pulse ox 
#   - etc, etc
class Patient(object): #TODO
    def __init__(self):
         self.name = ""
         self.age = 0
         self.bloodPressure = 0
         self.pulseOx = 0
         self.decisionTree = None