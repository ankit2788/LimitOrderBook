from abc import ABC, abstractclassmethod

from common import utils

class Tick():

    def __init__(self, data = None):
        """
        data -> a single tick (in list format)

        """

        if data is not None:
            self.timestamp      = data[4]
            self.messageType    = data[3]
            self.direction      = None
            self.isTrade        = False
            self.isBid          = False
        else:
            self.timestamp      = None
            self.messageType    = None
            self.direction      = None
            self.isTrade        = False
            self.isBid          = False

        

class TradeTick(Tick):
    def __init__(self, data):

        super().__init__(data)
        self.isTrade    = True
        self.bidOrderID = data[6]
        self.askOrderID = data[7]
        self.contract   = data[9] 
        self.price      = data[10]
        self.qty        = data[11]


class OrderTick(Tick):
    def __init__(self, data = None):

        super().__init__(data)
        self.isTrade    = False

        if data is not None:
            self.orderID    = data[6]
            self.contract   = data[8] 
            self.direction  = data[9]
            self.price      = data[10]
            self.qty        = data[11]
        else:
            self.orderID    = None
            self.contract   = None
            self.direction  = None
            self.price      = None
            self.qty        = None


    def __str__(self):
        if self.timestamp is not None:
            string = f"Time:{utils.GetReadableTime(self.timestamp)}\tContract:{self.contract}\tOrderID:{self.orderID}\tDir:{self.direction}\tPrice:{self.price}\tQty:{self.qty}"
        else:
            string = f"Time:{self.timestamp}\tContract:{self.contract}\tOrderID:{self.orderID}\tDir:{self.direction}\tPrice:{self.price}\tQty:{self.qty}"
        return string
        


class BidTick(OrderTick):

    def __init__(self, data = None):
        super().__init__(data = data) 
        self.isBid = True
    
class AskTick(OrderTick):

    def __init__(self, data = None):
        super().__init__(data) 
        self.isBid = False

        