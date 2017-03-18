from yapsy.IPlugin import IPlugin
from logbook.Importer import Plugin
import logging
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QCheckBox

class Default(IPlugin,Plugin):
    def __init__(self,log_name=None,event=None):
        self._actions='import'
        self._type='default'
        self.logging = logging.getLogger(__name__)
        self._filename = log_name                       # like test.gl
        self._event = event                             # like xyz.fit in database

    def open_logbook(self,logbook):
        pass
        
    def get_data(self,event):
        return TimeSeries([],[])
    
    def import_fit(self,fitfile=None):
        pass
        
    @property
    def ui(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("subjects"))
        layout.addWidget(QCheckBox("Physics"))
        layout.addWidget(QCheckBox("Maths"))
        return layout
    
    def connect(self,log_name=None,event=None):
        return Default(log_name,event)