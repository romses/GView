from yapsy.IPlugin import IPlugin
from logbook.Importer import Plugin
from messages import TimeSeriesData,TimeSeriesMetaData,LogMetaData
import logging
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QCheckBox

class Default(IPlugin,Plugin):
    def __init__(self,log_name=None,event=None):
        self._actions='import'
        self._type='default'
        self.logging = logging.getLogger(__name__)
        self._filename = log_name                       # like test.gl
        self._event = event                             # like xyz.fit in database
        self._metadata = None
        self._data = None

    def open_logbook(self,logbook):
        self._filename = logbook
        
    def import_fit(self,fitfile=None):
        pass
    
    def get_data(self,event):
        return TimeSeriesData([],[])
        
    @property
    def ui(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        return layout
    
    @property
    def metadata(self):
        return self._metadata
    
    @property
    def data(self):
        return self._data 

    def connect(self,event=None):
        return Default(log_name=self._filename,event=event)