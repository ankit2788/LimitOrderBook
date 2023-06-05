import time
from datetime import datetime


class MarketConstants():
    
    #Time
    START       = "09:15:00.000"
    END         = "15:30:00.000"


class DayConstants():

    def __init__(self, Date):
        '''
        Initializes Date parameters for one date (Ex: '20180404')
        '''
    
        self.Date           = Date

            
        self.MarketStart     = GenerateEpochTime(self.Date + " " + MarketConstants.START) 
        self.MarketEnd       = GenerateEpochTime(self.Date + " " + MarketConstants.END) 



def GenerateEpochTime(DateTime):
    #converts time into epoch format

    return int(time.mktime(time.strptime(DateTime, "%Y%m%d %H:%M:%S.%f")))*1000000

def GetReadableTime(TimeStamp):
    #timestamp in epoch (microsecs)
    
    return datetime.fromtimestamp(TimeStamp/1000000).time()
