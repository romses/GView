from yapsy.IPlugin import IPlugin
from messages import EventTableEntry,TimeSeries

class Plugin(IPlugin):
    
    def __init__(self):
        self._actions=None
        self._event=None

    def open_logbook(self,logbook=None):
        pass

    def test(self,fitfile=None,logbook=None):
        pass
        
    def import_fit(self,fitfile=None,logbook=None):
        pass
    
    def get_data(self,event):
        return (None)

    def get_metadata(self):
        pass
            
    @property
    def actions(self):
        return self._actions
    
    @property
    def event(self):
        return self._event

