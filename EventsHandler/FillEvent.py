from EventsHandler import Event

class ExchangeAcknowledgementEvent(Event):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        self.type = "ACK"
        self.clientOrderID = orderID
        self.contract = contract
        self.timestamp = timestamp
        self.direction = direction
        self.quantity = quantity
        self.price = price


    def print_fill(self):
        """
        Outputs the values within the Order.
        """
        print(f"Order: {self.clientOrderID} Symbol={self.contract}, Time={self.timestamp}\
            Quantity={self.quantity}, Direction={self.direction}, Price= {self.price}")


class NEW_ORDER_CONFIRM(ExchangeAcknowledgementEvent):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        super().__init__(contract, orderID, timestamp, direction, price, quantity)
        self.subtype = __class__.__name__

class NEW_ORDER_REJECT(ExchangeAcknowledgementEvent):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        super().__init__(contract, orderID, timestamp, direction, price, quantity)
        self.subtype = __class__.__name__

class CANCEL_ORDER_CONFIRM(ExchangeAcknowledgementEvent):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        super().__init__(contract, orderID, timestamp, direction, price, quantity)
        self.subtype = __class__.__name__

class CANCEL_ORDER_REJECT(ExchangeAcknowledgementEvent):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        super().__init__(contract, orderID, timestamp, direction, price, quantity)
        self.subtype = __class__.__name__

class MODIFY_ORDER_REJECT(ExchangeAcknowledgementEvent):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        super().__init__(contract, orderID, timestamp, direction, price, quantity)
        self.subtype = __class__.__name__

class MODIFY_ORDER_CONFIRM(ExchangeAcknowledgementEvent):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        super().__init__(contract, orderID, timestamp, direction, price, quantity)
        self.subtype = __class__.__name__

class TRADE_CONFIRM(ExchangeAcknowledgementEvent):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        super().__init__(contract, orderID, timestamp, direction, price, quantity)
        self.subtype = __class__.__name__
