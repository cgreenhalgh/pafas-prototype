# based on https://stackoverflow.com/questions/1904351/python-observer-pattern-examples-tips
 
class Event(object):
    """Basic event class"""
    pass

class Observable(object):
    """Common Obeservable"""
    def __init__(self):
        self.callbacks = []

    def subscribe(self, callback):
        """Callback to be called on fire with Event object"""
        self.callbacks.append(callback)
    
    def fire(self, type, value, **attrs):
        """Fire event -> call subscribed callbacks.
        
        Event has: source (self), type, value, other named attributes.
        Standard attributes are: oldvalue, TBC"""
        e = Event()
        e.source = self
        e.type = type
        e.value = value
        if attrs:
            for k, v in attrs.iteritems():
                setattr(e, k, v)
        for fn in self.callbacks:
            fn(e)