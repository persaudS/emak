# from model import DecisionTree
import tkinter as tk


class StartView:
    """StartView class for the start page of the GUI"""

    def __init__(self, root, nodeTitle):
        self.device_states = {}
        self.root = root
        self.root.title("MVC - EMAK")
        self.node = get_view_node(nodeTitle)

        # Create a label
        self.label = tk.Label(root, text="Hello, User!")
        self.label.pack(padx=20, pady=20)

        # Example button creation
        self.button = tk.Button(root, text="Click Here",
                                command=self.on_button_click)
        self.button.pack()
        self.root.mainloop()

    def on_button_click(self):
        self.label.config(text="Button Pressed!")
    
    def set_states(self, states):
        """Sets the states of the devices"""
        self.device_states = states
        #TODO: update view with new states
        return none
    
    def get_view_node(self, nodeTitle):
        """Gets the node view information from json file"""
        return none
    
    def start(self, states):
        """Starts the view"""
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = startView(root, "Start")
    root.mainloop()

    # print('MVC - the simplest example')
    # print('Do you want to see everyone in my db?[y/n]')
