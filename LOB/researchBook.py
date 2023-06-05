from LOB import orderBookManager
from importlib import reload

from common import utils
reload(orderBookManager)


class ResearchOrderBook(orderBookManager.OrderBook):

    def __init__(self, date):
        """
        date: dtype: str (YYYYMMDD)
        """
        self.millis_in_hour = 3600000
        self.millis_in_minute = 60000
        self.millis_in_second = 1000
        self.top_ask_price_cache = None
        self.top_bid_price_cache = None

        self.date = date
        objDay = utils.DayConstants(date)
        self.marketOpenTime     = objDay.MarketStart
        self.marketCloseTime    = objDay.MarketEnd

        self.BestBidCache = None
        self.BestAskCache = None




    def isMarketOpen(self):
        if self.lastTimeStamp >= self.marketOpenTime and self.lastTimeStamp <= self.marketCloseTime:
            return True
        return False
    

    @property
    def BestBid(self):
        if self.BestBidCache != None:
            return self.BestBidCache
        elif len(self.bidSide) == 0:
            return 0
        self.BestBidCache = self.bidSide.max()
        return self.BestBidCache

    @property
    def BestAsk(self):
        if self.BestAskCache != None:
            return self.BestAskCache
        elif len(self.askSide) == 0:
            return 0
        self.BestAskCache = self.askSide.min()
        return self.BestAskCache

    @property
    def BidVolume(self):
        return self.bidSide.volume

    @property
    def AskVolume(self):
        return self.askSide.volume

    @property
    def spread(self):
        spread = self.BestAsk - self.BestBid
        return spread if spread > 0 else 0

    @property
    def MidPrice(self):
        if self.spread > 0:
            return self.BestBid + (self.spread / 2)
        elif self.BestAsk > 0 and self.BestBid > 0:
            return self.BestBid
        else:
            return None

    @property
    def bids_order_count(self):
        return len(self.bidSide.orderMap)

    @property
    def asks_order_count(self):
        return len(self.askSide.orderMap)