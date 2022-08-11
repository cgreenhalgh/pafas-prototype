from tkinter import Frame, ttk, StringVar, OptionMenu, Canvas, messagebox
from time import time
from engine import Heartrate
from pygame import midi

class MidiOutFrame(Frame):
    """GUI frame for MIDI outout"""
    def __init__(self, master, heartrate):
        super().__init__(master)
        self.heartrate = heartrate
        self.heartrate.subscribe(self.heartrate_event)
        self.midiout = None # pygame.midi.Output
        self.midiout_name = None
        self.debug = False
        self.grid()
        ttk.Label(self, text="MIDI out:").grid(column=0, row=0)
        ttk.Button(self, text="Scan", command=self.scan).grid(column=1, row=0)
        self.midiout_var = StringVar(self)
        self.midiout_menu = OptionMenu(self, self.midiout_var, ())
        menu = self.midiout_menu["menu"]
        self.midiout_menu.configure(width=30)
        self.midiout_menu.grid(column=2,row=0)
        self.active = False
        self.status_canvas = Canvas(self, width=20, height=20)
        self.status_canvas.grid(column=3,row=0)
        self.await_status_inactive = None
        self.set_status(False,False)

    def select_midiout(self, midiout_name, index):
        """command handler to select specific midi output"""
        if not midiout_name:
            print('No midiout selected')
            self.midiout_var.set("None")
            self.close_midiout()
        else:
            print(f'select midiout {midiout_name}')
            self.midiout_var.set(midiout_name)
            if self.midiout_name == midiout_name:
                return
            self.close_midiout()
            print(f'Opening midi device {midiout_name} / {index}')
            try:
                self.midiout = midi.Output(index)
                self.midiout_name = midiout_name
                self.set_status(True,False)
            except Exception as err:
                print(f'Error opening midi output {index} ({midiout_name}): {err}')
                messagebox.showerror(title='Cannot open MIDI output', message=f'Error opening midi output {index} ({midiout_name}): {err}')

    def close_midiout(self):
        """Fast close current midi out (if any)"""
        if self.midiout:
            print(f'Closing midi out')
            self.midiout.abort()
            self.midiout = None
            self.midiout_name = None
            self.set_status(False,False)

    def set_status(self, open, active):
        """Update visual status indicator/flasher"""
        self.status_canvas.delete("all")
        if self.await_status_inactive:
            self.root().after_cancel(self.await_status_inactive)
            self.await_status_inactive = None
        if not open:
            self.status_canvas.create_rectangle(0, 0, 20, 20, fill="black")
        elif active:
            self.status_canvas.create_rectangle(0, 0, 20, 20, fill="red")
            self.root().after(300, lambda: self.set_status(True,False))
        else:
            self.status_canvas.create_rectangle(0, 0, 20, 20, fill="green")

    def root(self):
        """Get root (for after)"""
        s = self
        while s.master:
            s = s.master
        return s


    def scan(self):
        """scan for midi outputs and populate options"""
        midi.init()
        if not midi.get_init():
            print('ERROR: MIDI failed to initialise')
            return
        nmidi = midi.get_count()
        print(f'{nmidi} midi devices found')

        menu = self.midiout_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="None", command=lambda: self.select_midiout(None, -1))

        default_out = midi.get_default_output_id()
        midiout_exists = False
        for m in range(nmidi):
            #get_device_info(an_id) -> (interf, name, input, output, opened)
            info = midi.get_device_info(m)
            if not info:
                print(f'ERROR getting midi device {m} info')
            elif info[3]:
                print(f'Output {m}: {info[1]}')
                menu.add_command(label=info[1], command=lambda m=m, info=info: self.select_midiout(info[1], m))
                if self.midiout_name and self.midiout_name == info[1]:
                    midiout_exists = True

        if self.midiout and not midiout_exists:
            self.close_midiout()
        elif self.midiout and midiout_exists:
            pass
        else:
            self.select_midiout(None,-1)

    def heartrate_event(self, event):
        """Call back from Heartrate Observable"""
        if event.type == Heartrate.IBI_EVENT:
            self.send_midi_note(60)

    def send_midi_note(self, note):
        """Send specified note on"""
        if self.midiout:
            print(f'Send midi note {note}')
            self.midiout.note_on(note, velocity=127, channel=0)
            self.set_status(True,True)
        else:
            print(f'Note: no midi output; cannot send note {note}')