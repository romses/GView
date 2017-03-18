from sqlalchemy import *
import logging
from fitparse import FitFile
import os.path
from yapsy.PluginManager import PluginManager 
from messages import EventTableEntry,LogRow


'''
Created on 3 Mar 2017

@author: Christopher Kreitz
'''

class Logbook(object):
    '''
    classdocs
    '''

    def __init__(self, filename):
        '''
        Constructor
        '''
        self.logging = logging.getLogger(__name__)
        self.logging.debug("Logbook initialized")

        self.name = filename

        self._alchemy_logbook = create_engine('sqlite:///'+filename)

        self._metadata = MetaData(bind=self._alchemy_logbook)
        self._file_table = Table("file",self._metadata,
                                 Column('file_id',Integer,primary_key=True),
                                 Column('file_name',String(20)),
                                 Column('file_hash',String(64),unique=True),
                                 Column('creation_date',DateTime),
                                 Column('event_name',String(30)),
                                 Column('event_type',String(30)),
                                 Column('event_subtype',String(30))
                                 )
                
        self._check_database_integrity()
        
        self._plugins = {}
        
        try:
            manager = PluginManager()
            manager.setPluginPlaces(["logbook/Importer"])
            manager.collectPlugins()
        except Exception as e:
            print(e)
            
        '''
        load plugins and register them
        '''
        for p in manager.getAllPlugins():
            self.logging.info("loading plugin "+p.plugin_object.id)
            self._plugins[p.plugin_object.type]=p.plugin_object
            self._plugins[p.plugin_object.type].open_logbook(filename)

        self.logging.info("%s plugins loaded"%len(manager.getAllPlugins()))
        
        stmt = self._file_table.select().order_by(desc(self._file_table.c.creation_date))
        rows = stmt.execute()
        
        self.event_table = []
        
        '''
        create row objects.
        each event is connected to an object
        '''
        for row in rows:
            if row.event_type in self._plugins:
                o = self._plugins[row.event_type].connect(event=row)
            else:
                o = self._plugins['default'].connect(event=row)
            
            self.event_table.append(o)

    def close_logbook(self):
        self.event_table = []
#        self._file_table.close()
#        self._alchemy_logbook.close()

    def _check_database_integrity(self):
        '''
        Check the integrity of the logbook.
        
        - Check, if all tables are present
        '''
        
        self._metadata.create_all(checkfirst=True)
 
    def import_file(self,file):
                
        try:
            fitfile = FitFile(file)
            filename = os.path.basename(file)
            filehash = fitfile.digest
            
            creation_date = ""
            event_name = ""
            event_sport = ""
            event_subsport = ""

#            if not result:
            self.logging.info("Importing file %s",filename)
                
            for record in fitfile.get_messages():
                for record_data in record:
                    if record.name == "file_id" and record_data.name == "time_created":
                        creation_date = record_data.value
                    if record.name == "sport":
                        if record_data.name == "sport":
                            event_sport = str(record_data.value)
                        if record_data.name == "sub_sport":
                            event_subsport = str(record_data.value)
                        if record_data.name == "name":
                            event_name = record_data.value.decode('utf-8')
                            
            try:
                file_insert = self._file_table.insert()
                f_id = file_insert.values(file_name=filename,file_hash=filehash,
                                          creation_date=creation_date,event_name=event_name,
                                          event_type=event_sport, event_subtype=event_subsport)
                conn = self._alchemy_logbook.connect()
                conn.execute(f_id)
                if event_sport not in self._plugins:
                    self._plugins["default"].import_fit(fitfile)
                else:
                    self._plugins[event_sport].import_fit(fitfile)
                    
            except Exception as e:
                self.logging.info(e)
                
            self.logging.info("Import finished")
                
            return True
        except Exception as e:
#            self.logging.error("Error importing file")
            print(e)
            return False 
                    
    @property
    def events(self):
        return self.event_table

    def __getitem__(self,key):
        return self.event_table[key]