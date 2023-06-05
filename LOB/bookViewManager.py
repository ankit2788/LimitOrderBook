from io import StringIO
import threading
from queue import Queue
from importlib import reload

import LOB
from LOB import orderBookManager
import Indicators
from EventsHandler import MarketEvent
import multiprocessing

reload(MarketEvent)
reload(LOB)
reload(Indicators)
reload(orderBookManager)

from common import loggingConfig


logger = loggingConfig.logging
logger.getLogger("Book Runner")


class BookSubscriber(orderBookManager.OrderBook):
    def __init__(self, tickFile):
        logger.info(f'Creating TBT Data Iterator')
        self.myiter = LOB.tickCSVIterator(tickFile = tickFile, date = "20180404")
        self.run = True

        self.book = super().__init__()

    
    





class BookPlayer(orderBookManager.OrderBook):

    def __init__(self, tickFile, marketeventQueue, isfinishedQueue):

        # tickfile = "/Users/ankitgupta/Documents/git/CodePractise/Trading System Practise/TBT Sample Data/SBIN_FutTicks.csv"
        logger.info(f'Creating TBT Data Iterator')
        self.myiter = LOB.tickCSVIterator(tickFile = tickFile, date = "20180404")
        self.events = marketeventQueue
        self.isFinished = isfinishedQueue
        self.isFinished.put(False)

        self.writer = BookWriter()


    def run(self, counter = 10000):

        self.threadName = threading.current_thread().name
        self.processName = multiprocessing.current_process().name

        
        thread = threading.Thread(target=self.createbook, args = [counter], daemon = True)
        thread.start()
        thread.join()
        
        logger.info(f'{self.processName}\{self.threadName} -- All Done. Total items in events queue: {self.events.qsize()}')
        # print(f'All Done. Total items in events queue: {self.events.qsize()}')

    


    def createbook(self, counter = 10000 ):
        """
        events --> all events queue
        """
        
        
        nexttick = next(self.myiter)
        count = 0
        # while nexttick:
        while count < counter:
            if nexttick.messageType is not None and nexttick.messageType in ["N", "M", "X", "T"]:

                # Process this tick as part of the book
                
                self.writer.processTick(tick=nexttick)
                # print(writer.wholeStr())
                objindicators = Indicators.Indicators()
                objindicators.compute(self.writer, levels = 3)

                # update the events
                if nexttick.isTrade:
                    # create market event for Trade tick
                    _event = MarketEvent.onTrade(timestamp=nexttick.timestamp, indicators = objindicators)
                    self.events.put(_event)
                    logger.info(f'{self.processName}\{self.threadName} -- Putting Trade Market Event. Qsize: {self.events.qsize()}')

                elif nexttick.isBid:
                    # Check if Best Bid has changed
                    # create market event for Trade tick
                    if self.writer.bidSide.maxPrice is not None:
                        if self.writer.bidSide.prevMaxPrice is None or self.writer.bidSide.maxPrice != self.writer.bidSide.prevMaxPrice:
                            _event = MarketEvent.onTrade(timestamp=nexttick.timestamp, indicators = objindicators)
                            self.events.put(_event)
                            logger.info(f'{self.processName}\{self.threadName} -- Putting Bid change Market Event. Qsize: {self.events.qsize()}')

                else :
                    # Check if Best Ask has changed
                    # create market event for Trade tick
                    if self.writer.askSide.minPrice is not None:
                        if self.writer.askSide.prevMinPrice is None or self.writer.askSide.minPrice != self.writer.askSide.prevMinPrice:
                            
                            _event = MarketEvent.onTrade(timestamp=nexttick.timestamp, indicators = objindicators)
                            self.events.put(_event)
                            logger.info(f'{self.processName}\{self.threadName} -- Putting Ask change Market Event. Qsize: {self.events.qsize()}')

                


                # check for market event

            nexttick = next(self.myiter)
            count += 1

        self.isFinished.put(True)





class BookViewer(orderBookManager.OrderBook):

    def __init__(self):
        super().__init__()


    def bidBookStr(self, levels = 10):
        """
        Prints top n levels of the Bid side of the book
        """
        # Efficient string concat
        file_str = StringIO()
        file_str.write("------- Bids --------\n")
        if self.bidSide != None and len(self.bidSide) > 0:
            for k, v in self.bidSide.pricetree.items(reverse=True):
                # need to reverse the Bid Side, highest bid is at the top
                file_str.write('%s' % v)

        return file_str.getvalue()

    def askBookStr(self, levels = 10):
        """
        Prints top n levels of the Bid side of the book
        """
        # Efficient string concat
        file_str = StringIO()
        file_str.write("------- Asks --------\n")
        if self.askSide != None and len(self.askSide) > 0:
            for k, v in self.askSide.pricetree.items():
                file_str.write('%s' % v)
                
        return file_str.getvalue()
    
    def tradesBookstr(self):
        # Efficient string concat
        file_str = StringIO()
        file_str.write("------ Trades ------\n")
        if self.trades != None and len(self.trades) > 0:
            num = 0
            for entry in self.trades:
                if num < 10:
                    file_str.write(str(entry.qty) + " @ " \
                                   + '%f' % (entry.price) \
                                   + " (" + str(entry.timestamp) + ")\n")
                    num += 1
                else:
                    break
        return file_str.getvalue()
    

class BookWriter(orderBookManager.OrderBook):

    def __init__(self):
        super().__init__()


    def wholeStr(self, levels=3):

        # get bid side and get ask side upto n levels
        # Information needed: Price, Qty, nbOrders at each level of the book

        file_str = StringIO()
        file_str.write(str(self.lastTimeStamp))
        file_str.write(",")

        # append the bid side
        bidSide = self.bidBookStr(levels = levels)[:-1]
        file_str.write(bidSide)
        file_str.write(",")

        # append the bid side
        askSide = self.askBookStr(levels = levels)[:-1]
        file_str.write(askSide)
        # file_str += askSide

        return file_str.getvalue()    


    def bidBookStr(self, levels = 5):
        """
        Prints top n levels of the Bid side of the book
        """
        # Efficient string concat
        file_str = StringIO()
        if self.bidSide != None:
        
            count = 0
            for k, priceOrderList in self.bidSide.pricetree.items(reverse=True):
                # need to reverse the Bid Side, highest bid is at the top
                count += 1
                file_str.write(f'{priceOrderList.price},{priceOrderList.volume},{priceOrderList.nbOrders}')
                file_str.write(',')
                if count >= levels:
                    break

            while count < levels:
                file_str.write(f'nan,nan,nan')
                file_str.write(',')
                count += 1

            file_str.write(f'{self.bidSide.maxPrice}')
            file_str.write(',')

            # file_str = file_str[:-1]

        return file_str.getvalue()

    def askBookStr(self, levels = 5):
        """
        Prints top n levels of the Ask side of the book
        """
        # Efficient string concat
        file_str = StringIO()
        if self.askSide != None:
            
            count = 0
            for k, priceOrderList in self.askSide.pricetree.items():
                # need to reverse the Bid Side, highest bid is at the top
                count += 1
                file_str.write(f'{priceOrderList.price},{priceOrderList.volume},{priceOrderList.nbOrders}')
                file_str.write(',')
                if count >= levels:
                    break

            while count < levels:
                file_str.write(f'nan,nan,nan')
                file_str.write(',')
                count += 1

            file_str.write(f'{self.askSide.minPrice}')
            file_str.write(',')

            
            # file_str = file_str[:-1]

        return file_str.getvalue()    
