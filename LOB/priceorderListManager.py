from io import StringIO

class OrderList():

    def __init__(self, price):

        """
        A doubly ended linked List to maintain different orders at a particular price
        Key methods/ attributes:
        1. Append a new order onto the list
        2. Modify an existing order
        3. Move an order to the end of the list
        4. Delete an order from the list

        5. Maintains the location of prev Order and next Order
        6. Maintains count of total orders at this price level, and total volume present at this level

        
        """

        self.price  = price
        self.volume = 0
        self.nbOrders = 0

        self.headOrder = None       # stores order of dtype: Order (from orderManager)
        self.tailOrder = None       # stores order of dtype: Order (from orderManager)

        self.last = None            # Keeps track of last order while iterating. of dtype Order



    def __len__(self):
        return self.nbOrders
    
    def __iter__(self):
        self.last = self.headOrder
        return self
    
    def __next__(self):
        if self.last is None:
            raise StopIteration
        else:
            return_val = self.last
            self.last = self.last.next_order
            return return_val
        

    def append_order(self, order):
        """
        append a new order onto the list. 
        Based on the price time priority, price doesnt matter since this list is of the same price. 
        We will append to the end of the list

        Inputs:
            order: dtype: Order (from orderManager)

        Time complexity of appending: O(1) >>> since appending to the end of list
        """

        if self.nbOrders == 0:
            order.next_order = None
            order.prev_order = None

            self.headOrder = order
            self.tailOrder = order

        else:
            order.prev_order = self.tailOrder
            order.next_order = None

            # update the tail of this linked list with the new order
            self.tailOrder.next_order = order
            self.tailOrder = order

        self.nbOrders += 1
        self.volume += order.quantity




    def delete_order(self, order):
        """
        deletes a particular order from the linked list
        Inputs:
            order: dtype: Order (from orderManager)

        Time complexity of deleting: O(1) >>> since doubly ended queue. 
        We know the order's exact position, by knowing its prev and next orders
        """

        # Find the location of this order in the list
        prev_order = order.prev_order
        next_order = order.next_order

        if prev_order is not None and next_order is not None:
            # this order is somewhere in the between
            prev_order.next_order, next_order.prev_order = next_order, prev_order

        elif next_order is not None:
            # prev order is None. This means that this order was the 1st order in the list
            next_order.prev_order = None
            self.headOrder = next_order

        elif prev_order is not None:
            # next Order is None. This means that this order was the last order in the list
            prev_order.next_order = None
            self.tailOrder = prev_order

        
        # update quantity and nb of orders
        self.nbOrders -= 1
        self.volume -= order.quantity


    def move_to_tail(self, order):
        """
        Moves a particular order to the end of the list
        This happens in case of change in order priority due to order modification
        Inputs:
            order: dtype: Order (from orderManager)

        Time complexity of moving to tail: O(1) >>> 1st delete the order from list. Then append the order onto list

        """

        prev_order = order.prev_order
        next_order = order.next_order

        if order.prev_order is not None:
            # this order is not the head order
            order.prev_order.next_order = order.next_order

        else:
            # this order was the head order
            self.headOrder = order.next_order

        if order.next_order is not None:
            # current order is not the last order
            order.next_order.prev_order = order.prev_order

            # set the previous tail order's next order to this order
            
            self.tailOrder.next_order = order
            # self.tailOrder, order.prev_order = order, self.tailOrder
            self.tailOrder  = order
            order.prev_order = self.tailOrder
            order.next_order = None


    def __str__(self):

        buffer = StringIO()
        for order in self:
            buffer.write("%s\n" % str(order))

        return buffer.getvalue()



