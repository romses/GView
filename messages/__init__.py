import collections

'''
Created on 15.03.2017

@author: kreitz
'''
       
EventTableEntry    = collections.namedtuple("EventTableEntry", "filehash date name maintype subtype")
'''
meta_data:    data for the mainwindow event table
form_data:    data for the event form
time_series:  array of TimeSeries for the chart
ui:           the event ui
'''
LogRow             = collections.namedtuple("LogRow", "meta_data form_data time_series ui")
MetaData           = collections.namedtuple("EventTableEntry", "filehash date name maintype subtype")
FormData           = collections.namedtuple("FormData", "field_name field_value field_unit")
TimeSeries         = collections.namedtuple("TimeSeries","metadata data")
TimeSeriesData     = collections.namedtuple("TimeSeriesData","name timestamp data unit")
TimeSeriesMetaData = collections.namedtuple("TimeSeriesMetaData","name value unit")