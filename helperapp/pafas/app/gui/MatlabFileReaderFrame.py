from tkinter import Frame, ttk, filedialog, StringVar, OptionMenu, Canvas
from os import path
from time import time
from engine import Heartrate

class Block():
    """Block of data from a data file"""
    def __init__(self, block):
        self.block = block
        self.rwave_timestamps = []
    def add_timestamp(self, ts):
        self.rwave_timestamps.append(ts)

# E.G.
# S014
# Breaths/Minute: 10.08
# Block 1
# R wave timestamps
# 1377
# ...
# Inhale marker timestamps
# 2

class MatlabFileReaderFrame(Frame):
    """GUI frame for reading Matlab files of heartbeats for testing"""
    def __init__(self, master, heartrate):
        super().__init__(master)
        self.heartrate = heartrate
        self.debug = False
        self.blocks = []
        self.block = None
        self.grid()
        ttk.Label(self, text="Data file:").grid(column=0, row=0)
        ttk.Button(self, text="Load...", command=self.load).grid(column=1, row=0)
        self.block_var = StringVar(self)
        self.block_menu = OptionMenu(self, self.block_var, ())
        self.block_menu.configure(width=10)
        self.block_menu.grid(column=2,row=0)
        self.playing = False
        self.after_next = None
        self.after_clear = None
        ttk.Button(self, text="Play", command=self.play).grid(column=3, row=0)
        ttk.Button(self, text="Stop", command=self.stop).grid(column=4, row=0)
        self.status_canvas = Canvas(self, width=20, height=20)
        self.status_canvas.grid(column=5,row=0)
        self.set_status(False)
        self.update_block_options()

    def update_block_options(self):
        """Update block menu options from self.blocks"""
        # TODO
        menu = self.block_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="None", command=lambda: self.select_block(None))
        for block in self.blocks:
            menu.add_command(label=f'Block {block.block}', 
                             command=lambda b=block: self.select_block(b))
        if len(self.blocks)==0:
            self.select_block(None)
        else:
            self.select_block(self.blocks[0])
            
    def select_block(self, block):
        """User selects a data block - get ready to play it"""
        self.stop()
        self.block = block
        self.block_time_offset = 0
        self.block_ix = 0
        if not block:
            print('No block selected')
            self.block_var.set("None")
        else:
            print(f'select block {block.block}')
            self.block_var.set(f'Block {block.block}')

    def load(self):
        """User asks to load a data file"""
        file = filedialog.askopenfilename(initialdir= path.dirname(path.dirname(path.dirname(path.dirname(__file__)))))
        if not file:
            return
        print(f'Open file {file}')
        self.stop()
        self.blocks = []
        block = None
        rwave = False
        with open(file) as f:
            lines = f.readlines()
            for line in lines:
                match line.split():
                    case ["Breaths/Minute:", bpm]:
                        print(f'breath/minute: {bpm}')
                        rwave = False
                    case ["Block", b]:
                        block = Block(b)
                        print(f'start block {b}')
                        self.blocks.append(block)
                        rwave = False
                    case ["R","wave","timestamps"]:
                        rwave = True
                    case ["Inhale","marker","timestamps"]:
                        rwave = False
                    case []:
                        pass
                    case [value]:
                        if value.startswith("S"):
                            print(f'Subject {value}')
                            rwave = False
                        elif value.isnumeric():
                            fvalue = float(value)
                            if rwave and block:
                                block.add_timestamp(fvalue)
                        else:
                            print(f'Warning: unexpected line: {line}')
                            rwave = False
                    case _:
                        print(f'Warning: unexpected line: {line}')
                        rwave = False
        print(f'Read {len(self.blocks)} blocks of data')
        self.update_block_options()

    def play(self):
        """User presses play"""
        if self.playing:
            self.stop()
            # restart
            self.block_ix = 0
            self.block_time_offset = 0
        if not self.block:
            print('Error: play with no block')
            return
        if len(self.block.rwave_timestamps) <2:
            print(f'Error: not enough data in block - {len(self.block.rwave_timestamps)} timestamps')
            return

        self.playing = True
        self.block_start_time = time() - self.block_time_offset
        self.block_time_offset = 0
        self.set_hb_timer()

    def set_hb_timer(self):
        """Work out time to next heartbeat and set timer"""
        now = time()
        if self.block_ix == 0:
            # skip first 
            self.block_start_time = now - 0.001*self.block.rwave_timestamps[0]
        self.next_ibi = self.block.rwave_timestamps[self.block_ix+1] - self.block.rwave_timestamps[self.block_ix]
        next_time = 0.001*self.block.rwave_timestamps[self.block_ix+1] + self.block_start_time
        delay = next_time - now
        if self.debug:
            print(f'ix={self.block_ix}: {self.block.rwave_timestamps[self.block_ix]} -> {self.block.rwave_timestamps[self.block_ix+1]} delay {delay} ')
        if delay<0:
            print(f'Warning: next HB in past, ix={self.block_ix+1}, at {next_time} vs {now}')
            delay = 0
        self.after_next = self.root().after(int(1000*delay), self.hb_timer)
        if self.debug:
            print(f'Next HB {self.block_ix} in {delay}s')

    def hb_timer(self):
        """Heartbeat now!"""
        print(f'File reader: IBI {self.next_ibi}')
        self.heartrate.fire_ibi(self.next_ibi)
        self.block_ix = self.block_ix+1
        if (self.block_ix+1 >= len(self.block.rwave_timestamps)):
            # loop
            print(f'Note: looping heart data')
            self.block_ix = 0
        self.set_status(True)
        self.after_clear = self.root().after(200, self.clear_timer)
        self.set_hb_timer()

    def clear_timer(self):
        """Turn off the HB status (so it flashes)"""
        self.set_status(False)
        self.after_clear = None

    def root(self):
        """Get root (for after)"""
        s = self
        while s.master:
            s = s.master
        return s

    def stop(self):
        """User stops playback"""
        if self.after_next:
            self.root().after_cancel(self.after_next)
            self.after_next = None
        if self.after_clear:
            self.root().after_cancel(self.after_clear)
            self.after_clear = None
        self.set_status(False)
        if not self.playing:
            return
        # pause, ready to resume
        now = time()
        if self.debug:
            print(f'stop at {now} with offset {self.block_time_offset} and start time {self.block_start_time}')
        self.block_time_offset = now - self.block_start_time
        self.playing = False

    def set_status(self, status):
        """Update visual status indicator/flasher"""
        self.status_canvas.delete("all")
        if status:
            self.status_canvas.create_rectangle(0, 0, 20, 20, fill="red")
        else:
            self.status_canvas.create_rectangle(0, 0, 20, 20, fill="black")

        