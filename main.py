from windows import Window
from dictionary import Dictionary


# if __name__ == "__main__":
#     w = Window()



from tkinter import *

win = Tk() 
win.geometry("300x200") 

w = Label(win, text ='StudyTonight', font = "90",fg="Navyblue") 
w.pack() 

with open("dict.txt", "r", encoding="utf-8") as file:
    textt = file.read()
	
msg = Message(win, text = textt) 
	
msg.pack() 

win.mainloop() 