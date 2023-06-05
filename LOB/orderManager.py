
class Order():

    def __init__(self, tick, order_list):
        """
        From the Tick object, create the Order object
        It acts as a Node of a doubly linked list. 
        This Node will maintain its previous order and next order, along with this Order attributes

        Inputs:
            tick: dtype <Tick>
            order_list: dtype <OrderList> list of all the orders under a particular limit price
        """

        self.tick = tick
        self.order_list = order_list
        self.prev_order = None      
        self.next_order = None


    def next_order(self):
        return self.next_order
    
    def prev_order(self):
        return self.prev_order
    
    @property
    def orderID(self):
        return self.tick.orderID
    
    @property
    def isBid(self):
        return self.tick.isBid


    @property
    def quantity(self):
        return self.tick.qty
        
    @property
    def price(self):
        return self.tick.price
    
    @property
    def direction(self):
        return self.tick.direction
    
    def updateQty(self, newQty, newtimeStamp):
        #if quantity is modified, then 
        #a. If modified qty is less than the previous qty, then No priority change
        #b. If modified qty = 0( same case as order cancellation), delete order   < JUST UPDATE the QTY to 0.
        #c. If modified qty is greater than the previous qty, then remove old order and place a new one

        if newQty > self.quantity and self.order_list.last != self:
            # Case c, i.e. modification corresponds to a larger quantity. 
            # this order priority goes down, and this order moves to the end of the list

            self.order_list.move_to_tail(self)

        self.order_list.volume = self.order_list.volume + (newQty - self.quantity)
        self.tick.timestamp = newtimeStamp
        self.tick.qty       = newQty


    def updatePrice(self, newPrice, newtimeStamp, new_order_list):
        # if price is modified
        # this order needs to be removed from existing order_list, 
        # and need to be moved to the new order list corresponding to the new price

        # Inputs:
        # 1. newPrice
        # 2. newtimeStamp
        # 3. new_order_list --> dtype: Order_list Corresponds to the order list of the new price

        oldTick             = self.tick
        oldTick.timestamp   = newtimeStamp
        oldTick.price       = newPrice

        # append the order as a new order onto the new order list
        newOrder = Order(oldTick, new_order_list)
        new_order_list.append_order(newOrder)

        # delete the order from older order_list
        self.order_list.delete_order(self)
        



    def __str__(self):
        string = f'{self.quantity}\t\t{self.price}'
        return string




    


        



        