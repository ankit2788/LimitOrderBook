import sys, os
cwd = os.getcwd()

mainPath = f'{cwd}/'
sys.path.append(mainPath)

from queue import Queue
from importlib import reload

import threading

import LOB
from LOB import orderBookManager
from LOB import bookViewManager
import Indicators
from EventsHandler import MarketEvent
import multiprocessing
from FileReader import tickCSVIterator

reload(MarketEvent)
reload(LOB)
reload(Indicators)
reload(orderBookManager)
reload(bookViewManager)
reload(bookViewManager)


from common import loggingConfig


logger = loggingConfig.logging
logger.getLogger("Main")








def main():

    tickfile = "/Users/ankitgupta/Documents/STUDY/Trading System Practise/TBT Sample Data/SBIN_FutTicks.csv"
    marketeventqueue = Queue()
    signaleventQueue = Queue()
    bookFinishedQueue = Queue()

    

    # bookplayer = bookViewManager.BookPlayer(tickFile=tickfile, marketeventQueue=marketeventqueue, isfinishedQueue = bookFinishedQueue)
    # strategyRunner = BaseStrategy.BaseStrategy(contract = "SBIN18APRFUT", orderbook=bookplayer.writer, events=signaleventQueue)

    book = bookViewManager.BookWriter()
    iterator = tickCSVIterator(tickfile, date="20180404")

    tick = next(iterator)

    while tick:
        book.processTick(tick)
        print(book.wholeStr())
        tick = next(iterator)

        # print(writer.wholeStr())



    # bookplayer.run(counter = 10000)
    # strategyRunner.run(marketeventqueue = marketeventqueue, isFinishedqueue = bookFinishedQueue)


if __name__ == "__main__":

    main()




