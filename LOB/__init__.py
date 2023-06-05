
import pandas as pd
from common import utils
from LOB.tickManager import AskTick, BidTick, TradeTick, OrderTick
import numpy as np

class tickCSVIterator():
    """
    reads the csv file storing TBT information, and yields one row at a time

    """

    def __init__(self, tickFile, date):
        """
        tickFile: csv file for tick data
        date: YYYYMMDD format (string)
        """
                
        data                = pd.read_csv(tickFile, header = None)
        self.iterdata       = iter(data.values.tolist())
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
                        _thisTick = TradeTick(row)
                    else:
                        # order Tick
                        
                        if row[9] == "B":
                            _thisTick = BidTick(row)
                        else:
                            _thisTick = AskTick(row)

                        # if _thisTick.price <= 0:
                        #     return OrderTick()

                    return _thisTick

        except:
            raise StopIteration
        



class WriteOrderBook():
    """
    Writes OrderBook Snapshot to a file
    """

    def __init__(self, OutputFile):
        self.File = open(OutputFile, "w")
        
    def WriteToFile(self, Time, Information, NbLevels):

        BookInfo = [Time]
        BookInfo += self._WriteInformationOrderBook(Information[0], NbLevels)
        BookInfo += self._WriteInformationOrderBook(Information[1], NbLevels)

        super().WriteToFile(BookInfo)

    def CloseFile(self):
        self.File.close()

    @staticmethod
    def _WriteInformationOrderBook(Side, Levels):
    
        #available levels 
        combo = []
        
        if np.all(np.isnan(Side[0])):
            avail = 0
        else:
            avail = len(Side[0])
            
        for item in range(Levels):
            if avail == 0:
                combo += [np.nan,np.nan,np.nan]    
            
            else:
                if item < avail:
                    combo += [Side[0][item], Side[1][item], Side[2][item]]
                
                else:
                    combo += [np.nan,np.nan,np.nan]    
                    
                    
        return combo        