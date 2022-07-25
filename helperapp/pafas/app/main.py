from tkinter import Tk, Menu, filedialog, ttk, Frame
from os import path

# top-level window
root = Tk()
root.title("PAFAS app")

# set up menu options
menu = Menu(root)

def open():
    file = filedialog.askopenfilename(initialdir= path.dirname(path.dirname(path.dirname(__file__))))
    if not file:
        return
    print(f'Open file {file}')

open_item = Menu(menu)
open_item.add_command(label='Open', command=open)
menu.add_cascade(label='File', menu=open_item)
root.config(menu=menu)

# Main window content
class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        ttk.Label(self, text="Hello World!").grid(column=0, row=0)
        ttk.Button(self, text="Quit", command=root.destroy).grid(column=1, row=0)
        self.pack()

frm = App(root)

# run the app...
root.mainloop()
