from text_filter import TextFilter
from dictionary import Dictionary

class Finder(TextFilter, Dictionary):
    def __init__(self, dict_name, text_name):
        Dictionary.__init__(self, dict_name)
        TextFilter.__init__(self, text_name)
        self.new_words = []

        dic = self.get_dictionary()
        words = self.get_words()

        for x in words:
            if x not in dic:
                self.new_words.append(x)
    
    def get_new_words(self):
        return self.new_words



from tkinter import *

def p():
    index = listbox.curselection()[0]
    print(listbox.curselection())
    print(listbox.get(index))

def pp():
    listbox.activate(2)
    index = listbox.curselection()[0]
    print(listbox.get(index))
    # listbox.delete(0)

top = Tk()

top.geometry("200x250")

lbl = Label(top, text="List of Programming Languages")
btn = Button(text="petro", command=p)
btn.pack()
btnn = Button(text="Get word", command=pp)
btnn.pack()

listbox = Listbox(top)

f = Finder("dict.txt", "text.txt")

n = 0
for x in f.get_new_words():
    listbox.insert(n, x)
    n += 1

lbl.pack()
listbox.pack()
top.mainloop()
  