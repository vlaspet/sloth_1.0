from    tkinter import *


class Window:
    def __init__(self):
        self.tk =  self.tk()



class Viewer(Window):
    def __init__(self):
        self.tk =  self.tk()
        # widgets

        self.tk.title("Pure")
        self.tk.resizable(1, 1)
        self.tk.geometry("400x300+10+10")
        self.tk.mainloop()


class Extrator:
    pass


class Database(Extrator):
    pass

class Gamelogic(Database, Viewer):
    pass

vw = Viewer()