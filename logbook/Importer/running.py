from yapsy.IPlugin import IPlugin
from logbook.Importer import Plugin
from messages import TimeSeriesData,TimeSeriesMetaData,LogMetaData
from sqlalchemy import *
import logging
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit
#from PyQt5 import QtCore, QtGui, QtWidgets


class Running(IPlugin,Plugin):
    
    def __init__(self,log_name=None,metadata=None):
        self._actions=['import']
        self._type=['running']
        self.logging = logging.getLogger(__name__)
        self._filename = log_name
        self._formdata = None
        self._data = None
        self._metadata = None
        self.labels=[]
        self.lineedits = []
        
        if metadata:
            self._metadata = LogMetaData(file_hash=metadata.file_hash,
                                 date=metadata.creation_date,
                                 name=metadata.event_name,
                                 maintype=metadata.event_type,
                                 subtype=metadata.event_subtype
                                 )
            self.open_logbook(self._filename)
            self.get_data()

    def open_logbook(self,logbook):
        self._filename = logbook
        self._alchemy_logbook = create_engine('sqlite:///'+logbook)   
        _metadata = MetaData(bind=self._alchemy_logbook)
        
        self.file_table = Table('file', _metadata, autoload=True)
        self.swim_table = Table("event_running",_metadata,
                                Column('event_running_id',Integer,primary_key=True),
                                Column('f_id',Integer,ForeignKey("file.file_id"), nullable=False),
                                Column('timestamp',DateTime),
                                Column('cadence',Integer),
                                Column('distance',Integer),
                                Column('enhanced_speed',Float),
                                Column('heart_rate',Integer)
                                )
        self.swim_table.create(checkfirst=True)

    def import_fit(self,fitfile=None):
        stmt = self.file_table.select(self.file_table.c.file_hash==fitfile.digest)
        row = stmt.execute().fetchone()
        
        file_id = row.file_id
                
        for record in fitfile.get_messages(["record"]):
            timestamp = None
            cadence = None
            distance = None
            enhanced_speed = None
            heart_rate = None
            
            data = []
            
            for record_data in record:
                if record_data.name == "timestamp":
                    timestamp = record_data.value
                if record_data.name =="cadence":
                    cadence = record_data.value
                if record_data.name == "distance":
                    distance = record_data.value
                if record_data.name == "enhanced_speed":
                    enhanced_speed = record_data.value
                if record_data.name == "heart_rate":
                    heart_rate = record_data.value
                    
            data.append({'f_id':file_id,'timestamp':timestamp,
                         'cadence':cadence,'distance':distance,
                         'enhanced_speed':enhanced_speed,'heart_rate':heart_rate})
            

            self._alchemy_logbook.execute(self.swim_table.insert(),data)


    def get_data(self):
        
        s = self.swim_table.join(self.file_table).\
        select().where(self.file_table.c.file_hash==self._metadata.file_hash)

        cadence    = TimeSeriesData(name="cadence"   ,labels=[],data=[],unit='rpm')
        distance   = TimeSeriesData(name="distance"  ,labels=[],data=[],unit='m')
        heart_rate = TimeSeriesData(name="heart_rate",labels=[],data=[],unit="bpm")
        speed      = TimeSeriesData(name="speed"     ,labels=[],data=[],unit="m/s")
        
        rows = 0

#        cadence.data.append(0)
#        cadence.labels.append(0)

#        distance.data.append(0)
#        distance.labels.append(0)
        
#        heart_rate.data.append(0)
#        heart_rate.labels.append(0)
        
#        speed.data.append(0)
#        speed.labels.append(0)

        abs_len = 0
        last_ts = 0

        row = None
               
        for row in self._alchemy_logbook.execute(s):
            if row.cadence and row.distance and row.enhanced_speed and row.heart_rate:
                rows = rows + 1
                
                if last_ts == 0:
                    last_ts = row.timestamp

                ts =  ((row.timestamp-last_ts).seconds/60)

                
                cadence.data.append(row.cadence)
                cadence.labels.append(ts)
                
                distance.data.append(row.distance-abs_len)
                abs_len = row.distance
                distance.labels.append(ts)
                
                heart_rate.data.append(row.heart_rate)
                heart_rate.labels.append(ts)
                
                speed.data.append(row.enhanced_speed)
                speed.labels.append(ts)
            
        if row:
            self._data = [cadence,distance,heart_rate,speed]
    
            self._formdata = []
    
            self._formdata.append(TimeSeriesMetaData("Total Length",row.distance,"m"))
            self._formdata.append(TimeSeriesMetaData("Time per 100m","%.1f" %1,"s"))
            self._formdata.append(TimeSeriesMetaData("average speed","%.1f" %(1/1),"m/s"))
            self._formdata.append(TimeSeriesMetaData("Total calories",1,"kcal"))
            self._formdata.append(TimeSeriesMetaData("Event duration","%.1f" %(1),"min"))

    @property
    def ui(self):
        layout = QFormLayout()
        self.labels=[]
        self.lineedits=[]
        if self._formdata:
            for i in range(len(self._formdata)):
                layout.addRow(QLabel(self._formdata[i].name+" ("+self._formdata[i].unit+")"), QLineEdit(str(self._formdata[i].value)))
        return layout

    @property
    def metadata(self):
        return self._metadata
    
    @property
    def data(self):
        return self._data
    
    def connect(self,event=None):
        return Running(log_name=self._filename,metadata=event)