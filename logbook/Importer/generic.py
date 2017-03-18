from yapsy.IPlugin import IPlugin
from messages import TimeSeries,TimeSeriesData
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QCheckBox

class Generic(IPlugin):
    
    def __init__(self,log_name=None,event=None):
        self._actions='generic'
        self._type='generic'
        self._filename = log_name                       # like test.gl
        self._event = event                             # like xyz.fit in fatabase

    def open_logbook(self,logbook):
        pass
        
    def get_data(self,event):
        return TimeSeries([],[])
    
    def import_fit(self,fitfile=None):
        pass
            
    @property
    def actions(self):
        return self._actions
    
    @property
    def type(self):
        return self._type
        
    @property
    def ui(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        return layout
    
    @property
    def metadata(self):
        pass
    
    def get_event(self,log_name=None,event=None):
        print(log_name)
        return Generic(log_name,event)