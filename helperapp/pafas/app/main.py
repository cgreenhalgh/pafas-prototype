from tkinter import Tk, Menu, filedialog, ttk, Frame
from os import path
from gui import MatlabFileReaderFrame, MidiOutFrame
from engine import Heartrate

# top-level window
root = Tk()
root.title("PAFAS app")

# set up menu options
menu = Menu(root)

root.config(menu=menu)

# internal observable
heartrate = Heartrate()

# Main window content
class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        # test
        ttk.Label(self, text="Hello World!").grid(column=0, row=0)
        # file loader
        mfr = MatlabFileReaderFrame(self, heartrate)
        mfr.grid(sticky="W", column=0,row=1)
        mo = MidiOutFrame(self, heartrate)
        mo.grid(sticky="W", column=0,row=2)
        open_item = Menu(menu)
        open_item.add_command(label='Load data file...', command=mfr.load)
        open_item.add_command(label='Quit', command=root.destroy)
        menu.add_cascade(label='File', menu=open_item)
        self.pack()

frm = App(root)

# test...
heartrate.subscribe(lambda event: print(f'HB event: IBI {event.value}'))

# run the app...
root.mainloop()
