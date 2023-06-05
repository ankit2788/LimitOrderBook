from collections import deque
import pandas as pd
from io import StringIO
from importlib import reload
import numpy as np

from LOB import tickManager
from LOB import orderManager
from LOB import bookTree

reload(tickManager)
reload(orderManager)
reload(bookTree)






 
class OrderBook():

    def __init__(self):
        """
        Object to construct the order book

        Creates 2 trees each for Bid and Ask
        Key methods:
        1. process an incoming order tick
        2. process an incoming trade tick        
        """

        self.bidSide = bookTree.OneSideBook()        # Bid/ Ask side of the book is constructed using Binary Tree 
        self.askSide = bookTree.OneSideBook()        # Bid/ Ask side of the book is constructed using Binary Tree 
        self.lastTick = None
        self.lastTimeStamp = 0
        self.trades = deque(maxlen=1000)

        # # Create the tickdataIterator object and iterate over it
        # tickdata        = tickCSVIterator(tickFile=TBTDataFile)
        # self.iterTick   = iter(tickdata)


    def processTick(self, tick):
        """
        processes an incoming Tick and arranges it either onto Bid Side or Ask Side of the book. 
        In case of a Trade tick, treatment is different

        Inputs:
            tick: dtype <Tick>
    
        """

        # print(tick)
        if tick.price > 0:
            # process only when price is reasonable
            

            if tick.isTrade:
                # Trade tick processing
                self.processTradeTick(tick)

            else:
                # get the tree object (either Bid side or ask side)
                tree = self.askSide
                if tick.isBid:
                    # Bid Order tick 
                    tree = self.bidSide

                # if tick.timestamp > self.lastTimeStamp:
                tree.processTick(tick = tick)
                self.lastTimeStamp = tick.timestamp
                self.lastTick = tick



    def processTradeTick(self, tick):
        # Only processes Trade tick
        if tick.isTrade:

            # process both sides of the book simultaneously
            self._processTradeTickPerSide(tick, isBid=True)
            self._processTradeTickPerSide(tick, isBid=False)

            if tick.timestamp > self.lastTimeStamp:
                self.lastTimeStamp = tick.timestamp
            self.lastTick = tick
            self.trades.appendleft(tick)



    def _processTradeTickPerSide(self, tick, isBid = False):
        
        # Get the tree side, whether Bid or Ask
        bookSideTree = self.askSide

        # create a new tick. Either a Bid Tick or Ask Tick
        sideTick = tickManager.AskTick()
        # sideTick = tickManager.OrderTick()
        sideTick.direction = "S"
        sideTick.orderID = tick.askOrderID

        if isBid:
            sideTick = tickManager.BidTick()
            sideTick.direction = "B"
            sideTick.orderID = tick.bidOrderID

            bookSideTree = self.bidSide

        # search for the sideTick Order ID in corresponding Tree
        if sideTick.orderID in bookSideTree.orderMap:
            _originalQty = bookSideTree.orderMap[sideTick.orderID].quantity

            sideTick.contract = tick.contract
            sideTick.timestamp = tick.timestamp
            sideTick.price      = tick.price

            # reduce the quantity of older order, since part of it is now matched
            sideTick.qty        = _originalQty - tick.qty
            if sideTick.qty > 0:
                sideTick.messageType = "M"   #Modifies the older tick
            else:
                sideTick.messageType = "X"   #delete the older tick

            # create an order message based on this tick

            bookSideTree.processTick(tick = sideTick)


    def __str__(self):
        # Efficient string concat
        file_str = StringIO()
        file_str.write("------ Bids -------\n")

        if self.bidSide != None and len(self.bidSide) > 0:
            for k, v in self.bidSide.pricetree.items(reverse=True):
                file_str.write('%s' % v)

        file_str.write("\n------ Asks -------\n")
        if self.askSide != None and len(self.askSide) > 0:
            for k, v in self.askSide.pricetree.items():
                file_str.write('%s' % v)

        file_str.write("\n------ Trades ------\n")
        if self.trades != None and len(self.trades) > 0:
            num = 0
            for entry in self.trades:
                if num < 5:
                    file_str.write(str(entry.qty) + " @ " \
                                   + str(entry.price) \
                                   + " (" + str(entry.timestamp) + ")\n")
                    num += 1
                else:
                    break
        file_str.write("\n")
        return file_str.getvalue()
        

    def getTopNLevels(self, levels=3):
        return self.__getTopNLevelsBidSide(levels), self.__getTopNLevelsAskSide(levels)

    def __getTopNLevelsBidSide(self, levels=3):

        bidSide = self.bidSide
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

    def __getTopNLevelsAskSide(self, levels=3):

        askSide = self.askSide
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

    @property
    def bestBid(self):
        if self.bidSide.volume > 0:
            return self.bidSide.maxPrice
        return np.nan
    
    @property
    def bestAsk(self):
        if self.askSide.volume > 0:
            return self.askSide.minPrice
        return np.nan
    
    @property
    def spread(self):
        if self.askSide.volume > 0 and self.bidSide.volume > 0:
            return self.bestAsk - self.bestBid
        return np.nan
    
    @property
    def midPrice(self):
        if self.askSide.volume > 0 and self.bidSide.volume > 0:
            # print(self.lastTimeStamp, self.bestAsk, self.bestBid)
            return (self.bestAsk + self.bestBid)/2
        elif self.askSide is not None:
            return self.bestAsk
        elif self.bidSide is not None:
            return self.bestBid
        
        return np.nan    
    
    @property
    def LTP(self):
        if len(self.trades) > 0:
            return self.trades[0].price
        return np.nan 
    
    @property
    def bidVolume(self):
        if self.bidSide.volume > 0:
            return self.bidSide.volume        
        return 0
    
    @property
    def bestBidVolume(self):
        if self.bidSide.volume > 0:
            maxprice = self.bestBid
            priceMap = self.bidSide.getPriceMap(maxprice)
            return priceMap.volume
        return 0

    @property
    def bestAskVolume(self):
        if self.askSide.volume > 0:
            minprice = self.bestAsk
            priceMap = self.askSide.getPriceMap(minprice)
            return priceMap.volume
        return 0

    @property
    def askVolume(self):
        if self.askSide.volume > 0:
            return self.askSide.volume        
        return 0
    
    @property
    def bidOrderCounts(self):
        if self.bidSide.volume > 0:
            return len(self.bidSide.orderMap)
        return 0

    @property
    def askOrderCounts(self):
        if self.askSide.volume > 0:
            return len(self.askSide.orderMap)
        return 0

    @property
    def totalOrders(self):
        return self.bidOrderCounts + self.askOrderCounts
    
    @property
    def volImbalance(self):
        return self.bidVolume - self.askVolume
    

    @property
    def isTrade(self):
        if self.lastTick.isTrade:
            return True
        return False

    @property
    def vwap(self):
        """
        Volume weighted average price
        """

        bid_vol = self.bidVolume
        ask_vol = self.askVolume
        vol = bid_vol + ask_vol

        midPrice = self.midPrice
        
        if bid_vol == 0 or ask_vol == 0:
            return midPrice
        
        ratio = ask_vol/vol
        bestBid = self.bestBid
        return bestBid + (self.spread * ratio)







            



    


     


    
