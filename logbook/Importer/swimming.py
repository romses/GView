from yapsy.IPlugin import IPlugin
from logbook.Importer import Plugin
from messages import TimeSeriesData,TimeSeriesMetaData,LogMetaData
from sqlalchemy import *
import logging
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QFormLayout, QLineEdit, QRadioButton


class Swimming(IPlugin,Plugin):
    
    def __init__(self,log_name=None,metadata=None):
        self._actions='import'
        self._type='swimming'
        self.logging = logging.getLogger(__name__)
        self._filename = log_name
        self._formdata = None
        self._data = None
        self._metadata = None
        
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
        self.swim_table = Table("event_swimming",_metadata,
                                Column('event_swimming_id',Integer,primary_key=True),
                                Column('f_id',Integer,ForeignKey("file.file_id"), nullable=False),
                                Column('event_timestamp',DateTime),
                                Column('start_time',DateTime),
                                Column('swim_stroke',String(30)),
                                Column('total_calories',Integer),
                                Column('total_elapsed_time',Float),
                                Column('total_strokes',Integer),
                                Column('distance',Integer)
                                )
        self.swim_table.create(checkfirst=True)

    def import_fit(self,fitfile=None):
        stmt = self.file_table.select(self.file_table.c.file_hash==fitfile.digest)
        row = stmt.execute().fetchone()
        
        file_id = row.file_id
                
        for record in fitfile.get_messages(["length"]):
            event_timestamp = None
            start_time = None
            swim_stroke = None
            total_calories = None
            total_elapsed_time = None
            total_strokes = None
            distance=None
            
            data = []
            
            for record_data in record:
                if record_data.name == "timestamp":
                    event_timestamp = record_data.value
                if record_data.name =="start_time":
                    start_time = record_data.value
                if record_data.name == "swim_stroke":
                    swim_stroke = record_data.value
                if record_data.name == "total_calories":
                    total_calories = record_data.value
                if record_data.name == "total_strokes":
                    total_strokes = record_data.value
                if record_data.name == "total_elapsed_time":
                    total_elapsed_time = record_data.value

            data.append({'f_id':file_id,'event_timestamp':event_timestamp,
                         'start_time':start_time,'swim_stroke':swim_stroke,
                         'total_calories':total_calories,'total_elapsed_time':total_elapsed_time,
                         'total_strokes':total_strokes})
            

            self._alchemy_logbook.execute(self.swim_table.insert(),data)

        data=[]
        for record in fitfile.get_messages(["record"]):
            for record_data in record:
                if record_data.name == "timestamp":
                    event_timestamp = record_data.value
                if record_data.name == "distance":
                    distance = record_data.value

            data.append({'timestamp':event_timestamp,'distance':distance})

            stmt = self.swim_table.update().\
            where(self.swim_table.c.event_timestamp==bindparam('timestamp')).\
            values(distance=bindparam('distance'))
            self._alchemy_logbook.execute(stmt,data)

    def get_data(self):
        
        s = self.swim_table.join(self.file_table).\
        select().where(self.file_table.c.file_hash==self._metadata.file_hash)

        strokes_data  = TimeSeriesData(name="strokes" ,labels=[],data=[],unit=None)
        calories_data = TimeSeriesData(name="calories",labels=[],data=[],unit=None)
        speed_data    = TimeSeriesData(name="speed"   ,labels=[],data=[],unit="min/100m")
        
        rows = 0
        total_calories = 0
        event_duration = 0

        strokes_data.data.append(0)
        strokes_data.labels.append(0)
        
        calories_data.data.append(0)
        calories_data.labels.append(0)
        
        speed_data.data.append(0)
        speed_data.labels.append(0)

        row = None
               
        for row in self._alchemy_logbook.execute(s):
            if row.total_strokes and row.distance and row.total_calories and row.total_elapsed_time:
                rows = rows + 1
                strokes_data.data.append(row.total_strokes)
                strokes_data.labels.append(row.distance)
                
                calories_data.data.append(row.total_calories)
                calories_data.labels.append(row.distance)
                
                speed_data.data.append(((row.total_elapsed_time/50)*100)/60) #FIXME
                speed_data.labels.append(row.distance)
                
                total_calories = total_calories + row.total_calories
                event_duration = event_duration + row.total_elapsed_time
            
        if row:
            lap_distance = row.distance / rows
            total_length = row.distance
            total_time = row.start_time
            
            self._data = [strokes_data,calories_data,speed_data]
            
            time_per_hundred = (100/lap_distance)*(event_duration/lap_distance)
    
            self._formdata = []
    
            self._formdata.append(TimeSeriesMetaData("Lap length",lap_distance,"m"))
            self._formdata.append(TimeSeriesMetaData("Total Length",total_length,"m"))
            self._formdata.append(TimeSeriesMetaData("Time per 100m",time_per_hundred,"s"))
            self._formdata.append(TimeSeriesMetaData("average speed",(total_length/event_duration),"m/s"))
            self._formdata.append(TimeSeriesMetaData("Total time",total_time,"s"))
            self._formdata.append(TimeSeriesMetaData("Total calories",total_calories,"kcal"))
            self._formdata.append(TimeSeriesMetaData("Event duration",event_duration,"s"))

    @property
    def ui(self):
        layout = QFormLayout()
        sex = QHBoxLayout()
        sex.addWidget(QRadioButton("Male"))
        sex.addWidget(QRadioButton("Female"))
        layout.addRow(QLabel("Sex"),sex)
        layout.addRow("Date of Birth",QLineEdit())
        return layout

    @property
    def metadata(self):
        return self._metadata
    
    @property
    def data(self):
        return self._data
    
    def connect(self,event=None):
        return Swimming(log_name=self._filename,metadata=event)