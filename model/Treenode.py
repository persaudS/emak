#TreeNode is one of:
#    - an action (ex. read pulse)
#    - a question (ex. buttons)
#    - a visual demonstration (video)
class TreeNode:
    
    def __init__(self, id, text, options):
      self.id = id
      #Main text. For questions it will say something like "Please choose the
      #correct answer for the situation" and for actions it will describe the action
      self.text = text
      #String array containing the button text
      self.options = options
      
    #Returns the main text to display on the page
    def getText():
      return self.text
    #Returns the array of options for the view to display as buttons
    def getOptions():
      return self.options
   

    #Returns an instance of the next treenode. Value is passed by
    #the controller (or main model class) and informs the logic of this function as to which
    #treenode it should return (value may be the index of an option or vital readings)
    #The logic will be hardcoded for each node
    def getNextTreeNode(value):
      return None


   