from EventsHandler import Event

class SignalEvent(Event):
    def __init__(self, contract, timestamp, direction, bookIndicators):
        self.type = "SIGNAL"
        self.contract = contract
        self.timestamp = timestamp
        self.direction = direction
        self.bookIndicators = bookIndicators

    def __str__(self):
        string = f'SIGNAL:  {self.timestamp} --- {self.contract} --- {self.direction}'
        return string
