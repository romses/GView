from yapsy.IPlugin import IPlugin
from logbook.Importer import Plugin
from messages import TimeSeriesData,TimeSeriesMetaData,LogMetaData
import logging
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QCheckBox

class Default(IPlugin,Plugin):
    def __init__(self,log_name=None,metadata=None):
        self._actions='import'
        self._type='default'
        self.logging = logging.getLogger(__name__)
        self._filename = log_name                       # like test.gl
        self._metadata = None
        self._data = None
        
        if metadata:
            self._metadata = LogMetaData(file_hash=metadata.file_hash,
                                 date=metadata.creation_date,
                                 name=metadata.event_name,
                                 maintype=metadata.event_type,
                                 subtype=metadata.event_subtype
                                 )

    def open_logbook(self,logbook):
        self._filename = logbook
        
    def import_fit(self,fitfile=None):
        pass
    
    def get_data(self,event):
        self._data = [TimeSeriesData(name="dummy" ,labels=[],data=[],unit=None)]
        
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
        return Default(log_name=self._filename,metadata=event)