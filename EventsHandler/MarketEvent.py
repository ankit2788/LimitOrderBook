from EventsHandler import Event

class MarketEvent(Event):
    def __init__(self, timestamp, indicators):
        self.type = "MARKET"
        self.timestamp = timestamp
        self.indicators = indicators

class onTick(MarketEvent):
    def __init__(self, timestamp,indicators):
        super().__init__(timestamp,indicators)
        self.subtype = "New Tick"

class onTrade(MarketEvent):
    def __init__(self, timestamp,indicators):
        super().__init__(timestamp,indicators)
        self.subtype = "New Trade"

class onTimer(MarketEvent):
    def __init__(self, timestamp,indicators, fromLastTime):
        # fromLastTime in microseconds
        super().__init__(timestamp,indicators)
        self.subtype = f"Time since last tick {fromLastTime/1000000} secs"




class onBidChange(MarketEvent):
    def __init__(self, timestamp,indicators):
        super().__init__(timestamp,indicators)
        self.subtype = "BidChange"

class onAskChange(MarketEvent):
    def __init__(self, timestamp,indicators):
        super().__init__(timestamp,indicators)
        self.subtype = "AskChange"        

class onSpreadChange(MarketEvent):
    def __init__(self, change, timestamp,indicators):
        super().__init__(timestamp,indicators)
        self.subtype = f"Spread Update {change} points"

