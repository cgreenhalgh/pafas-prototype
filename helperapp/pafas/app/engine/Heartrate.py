from .Observable import Observable


class Heartrate(Observable):
    """Heartrate core model"""

    IBI_EVENT = "ibi"

    def __init__(self):
        Observable.__init__(self)

    def fire_ibi(self, ibi):
        """fire Observable IBI_EVENT
        
        i.e. new inter-beat interval = heartbeat."""
        self.fire(Heartrate.IBI_EVENT, ibi)
