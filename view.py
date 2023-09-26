# from model import DecisionTree
import tkinter as tk


class startView:
    def __init__(self, root):
        self.root = root
        self.root.title("MVC - EMAK")

        # Create a label
        self.label = tk.Label(root, text="Hello, User!")
        self.label.pack(padx=20, pady=20)

        # Example button creation
        self.button = tk.Button(root, text="Click Here",
                                command=self.on_button_click)
        self.button.pack()

    def on_button_click(self):
        self.label.config(text="Button Pressed!")


if __name__ == "__main__":
    root = tk.Tk()
    app = startView(root)
    root.mainloop()

    # print('MVC - the simplest example')
    # print('Do you want to see everyone in my db?[y/n]')
