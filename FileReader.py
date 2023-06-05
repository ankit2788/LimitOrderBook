from abc import ABC, abstractclassmethod
import pandas as pd
from common import utils
from LOB import tickManager
import numpy as np
# from MLModel import Snapshot


    



class CSVIterator(ABC):
    def __init__(self, file):

        data                = pd.read_csv(file, header = None)
        self.iterdata       = iter(data.values.tolist())

    @abstractclassmethod        
    def __iter__(self):
        return self
    
    @abstractclassmethod
    def __next__(self):
        pass





class tickCSVIterator(CSVIterator):
    """
    reads the csv file storing TBT information, and yields one row at a time

    """

    def __init__(self, tickFile, date):
        """
        tickFile: csv file for tick data
        date: YYYYMMDD format (string)
        """
        super().__init__(file=tickFile)
        self.date           = date
        self.market_end     = utils.DayConstants(date).MarketEnd
        self.market_start   = utils.DayConstants(date).MarketStart

    def __iter__(self):
        return self

        
    def __next__(self):
        try:            
            for row in self.iterdata:
                if row[4] >= self.market_start and row[4] <= self.market_end:
                    # Dont run for the ticks which are after market close and before market open
                    # print(row)
                    if row[3] == "T":
                        # this is a trade tick
                        _thisTick = tickManager.TradeTick(row)
                    else:
                        # order Tick
                        
                        if row[9] == "B":
                            _thisTick = tickManager.BidTick(row)
                        else:
                            _thisTick = tickManager.AskTick(row)

                    return _thisTick

        except:
            raise StopIteration


# class OrderBookCSVIterator(CSVIterator):
#     def __init__(self, OBFile, date):
#         """
#         tickFile: csv file for tick data
#         date: YYYYMMDD format (string)
#         """
#         super().__init__(file=OBFile)
#         self.date           = date
#         self.market_end     = utils.DayConstants(date).MarketEnd
#         self.market_start   = utils.DayConstants(date).MarketStart

#     def __iter__(self):
#         return self
    
#     def __next__(self):
#         try:            
#             for row in self.iterdata:
#                 thisSnap = Snapshot(row)
#                 if row.timestamp >= self.market_start and row.timestamp <= self.market_end:
#                     # Dont run for the ticks which are after market close and before market open
#                     # print(row)

#                     return thisSnap
#         except:
#             raise StopIteration    



