from EventsHandler import Event

class OrderEvent(Event):
    def __init__(self, contract, orderID, timestamp, direction, price, quantity):
        self.type = "ORDER"
        self.clientOrderID = orderID
        self.contract = contract
        self.timestamp = timestamp
        self.direction = direction
        self.quantity = quantity
        self.price = price



    def __str__(self):
        """
        Outputs the values within the Order.
        """
        string = f"Order: {self.clientOrderID} Symbol={self.contract}, Time={self.timestamp}\
            Quantity={self.quantity}, Direction={self.direction}, Price= {self.price}"
        
        return string
        

