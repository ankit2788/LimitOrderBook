from LOB.orderBookManager import OrderBook
import numpy as np



class Indicators():
    def compute(self, orderbook, levels = 3):
        self._bookDepth = self._getBookDepth(orderbook)
        self._bestBidAsk = self._getBestBidAskPrice(orderbook)
        self._midPrice = self._getMidPrice(orderbook)
        self._Spread = self._getSpread(orderbook)
        self._LTP = self._getLTP(orderbook)
        self._BidVolume = self._getBidSideVolume(orderbook)
        self._AskVolume = self._getAskSideVolume(orderbook)
        self._askOrders = self._orderCountAsks(orderbook)
        self._bidOrders = self._orderCountBids(orderbook)
        self._totalOrders = self._orderCountTotal(orderbook)
        self._vwap = self._vwap(orderbook)
        self._topNBids = self._getTopNBids(orderbook, levels)
        self._topNAsks = self._getTopNAsks(orderbook, levels)


    @property
    def topNBids(self):
        return self._topNBids

    @property
    def topNAsks(self):
        return self._topNAsks

    @property
    def bookDepth(self):
        return self._bookDepth


    @property
    def bookDepth(self):
        return self._bookDepth

    @property
    def bestBidAsk(self):
        return self._bestBidAsk
    @property
    def midPrice(self):
        return self._midPrice
    @property
    def Spread(self):
        return self._Spread
    @property
    def vwap(self):
        return self._vwap
    @property
    def totalOrders(self):
        return self._totalOrders
    @property
    def askOrders(self):
        return self._askOrders
    @property
    def bidOrders(self):
        return self._bidOrders
    @property
    def AskVolume(self):
        return self._AskVolume

    @property
    def BidVolume(self):
        return self._BidVolume
    @property
    def LTP(self):
        return self._LTP

    def _getTopNBids(self, orderbook, levels = 5):
        return getTopNBidSide(orderbook, levels)

    def _getTopNAsks(self, orderbook, levels = 5):
        return getTopNAskSide(orderbook, levels)

    def _getBookDepth(self, orderbook):
        return getBookDepth(orderbook)


    def _getBookDepth(self, orderbook):
        return getBookDepth(orderbook)

    def _getBestBidAskPrice(self, orderbook):
        return getBestBidAskPrice(orderbook)

    def _getMidPrice(self, orderbook):
        return getMidPrice(orderbook)

    def _getSpread(self, orderbook):
        return getSpread(orderbook)

    def _getLTP(self, orderbook):
        return getLTP(orderbook)

    def _getBidSideVolume(self, orderbook):
        return getBidSideVolume(orderbook)
        
    def _getAskSideVolume(self, orderbook):
        return getAskSideVolume(orderbook)
        
    def _orderCountBids(self, orderbook):
        return orderCountBids(orderbook)

    def _orderCountAsks(self, orderbook):
        return orderCountAsks(orderbook)

    def _orderCountTotal(self, orderbook):
        return orderCountTotal(orderbook)

    def _vwap(self, orderbook):
        return vwap(orderbook)
    


def getBookDepth(orderBook):
    """
    returns the length of bid and ask side of the book
    Inputs:
        orderBook: dtype <OrderBook>
    """

    if orderBook.bidSide is not None and orderBook.askSide is not None:
        return (len(orderBook.bidSide), len(orderBook.askSide))
    elif orderBook.bidSide is not None:
        return (len(orderBook.bidSide), 0)
    elif orderBook.bidSide is not None:
        return (0, len(orderBook.askSide))
    else:
        return (0,0)
    

def getTopNBidSide(orderBook, levels = 3):
    bidSide = orderBook.bidSide
    count = 0
    price = []
    volume = []
    orders = []
    if bidSide is not None:
        for k, priceOrderList in bidSide.pricetree.items(reverse=True):
            # need to reverse the Bid Side, highest bid is at the top
            price.append(priceOrderList.price)
            volume.append(priceOrderList.volume)
            orders.append(priceOrderList.nbOrders)

            count += 1
            if count >= levels:
                break

    return price, volume, orders


def getTopNAskSide(orderBook, levels = 3):
    askSide = orderBook.askSide
    count = 0
    price = []
    volume = []
    orders = []
    if askSide is not None:
        for k, priceOrderList in askSide.pricetree.items():
            # need to reverse the Bid Side, highest bid is at the top
            price.append(priceOrderList.price)
            volume.append(priceOrderList.volume)
            orders.append(priceOrderList.nbOrders)

            count += 1
            if count >= levels:
                break

    return price, volume, orders            

    


def getBestBidAskPrice(orderBook):
    """
    Inputs:
        orderBook: dtype <OrderBook>    
    """

    if orderBook.bidSide is not None and orderBook.askSide is not None:
        return orderBook.bidSide.maxPrice, orderBook.askSide.minPrice
    elif orderBook.bidSide is not None:
        return (orderBook.bidSide.maxPrice, np.nan)
    elif orderBook.bidSide is not None:
        return (np.nan, orderBook.askSide.minPrice)
    else:
        return (np.nan, np.nan)
    

def getMidPrice(orderBook):
    """
    Inputs:
        orderBook: dtype <OrderBook>    
    """
    try:
        if orderBook.bidSide is not None and orderBook.askSide is not None:
            return (orderBook.bidSide.maxPrice + orderBook.askSide.minPrice)/2
        elif orderBook.bidSide is not None:
            return orderBook.bidSide.maxPrice
        elif orderBook.askSide is not None:
            return orderBook.askSide.minPrice
        else:
            return np.nan
        
    except:
        return np.nan
        


def getSpread(orderBook):
    """
    Inputs:
        orderBook: dtype <OrderBook>    
    """
    try:

        if orderBook.bidSide is not None and orderBook.askSide is not None:
            return orderBook.askSide.minPrice - orderBook.bidSide.maxPrice 
        else:
            return np.nan   
    except:
        return np.nan
         

def getLTP(orderBook):
    """
    Inputs:
        orderBook: dtype <OrderBook>    
    """

    if len(orderBook.trades) > 0:
        return orderBook.trades[0].price
    else:
        return np.nan 

def getBidSideVolume(orderBook):
    if orderBook.bidSide is not None:
        return orderBook.bidSide.volume
    return 0

def getAskSideVolume(orderBook):
    if orderBook.askSide is not None:
        return orderBook.askSide.volume
    return 0


def getVolumeImbalance(orderBook):
    """
    Bid-ask volume imbalance
    Positive value indicates bid volume > ask volume
    Negative value indicates ask volume > bid volume
    Zero value indicates bid volume == ask volume    
    """
    if orderBook.bidSide is not None and orderBook.askSide is not None:
        return orderBook.bidSide.volume - orderBook.askSide.volume
    else:
        return np.nan

def orderCountBids(orderBook):
    """
    nb of orders on the bid side
    """
    if orderBook.bidSide is not None:
        return len(orderBook.bidSide.orderMap)
    return 0

def orderCountAsks(orderBook):
    """
    nb of orders on the Ask side
    """
    if orderBook.askSide is not None:
        return len(orderBook.askSide.orderMap)
    return 0
    
def orderCountTotal(orderBook):
    return orderCountAsks(orderBook) + orderCountBids(orderBook)

def vwap(orderBook):
    """
    Volume weighted average price
    """

    bid_vol = getBidSideVolume(orderBook)
    ask_vol = getAskSideVolume(orderBook)
    vol = bid_vol + ask_vol

    midPrice = getMidPrice(orderBook)
    
    if bid_vol == 0 or ask_vol == 0:
        return midPrice
    
    ratio = ask_vol/vol
    bestBid = getBestBidAskPrice(orderBook)[0]
    return bestBid + (getSpread(orderBook) * ratio)







    




