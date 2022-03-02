from tkinter import *
from view import Views


class Controller:
    def __init__(self, root):
        self.root_controller = root
        self.active_view()

    def active_view(self):
        Views(self.root_controller)


if __name__ == "__main__":
    root = Tk()
    app = Controller(root)
    root.mainloop()