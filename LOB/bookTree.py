
from bintrees import FastRBTree

from importlib import reload

from LOB import priceorderListManager
from LOB import orderManager

reload(priceorderListManager)
reload(orderManager)




class OneSideBook():

    def __init__(self):
        """
        A balanced binary tree data structure for either side of the book sorted by the price
        Main functions 
        1. Create a new price level
        2. Remove a price level
        3. Process an incoming Tick, i.e. update the order book accordingly
        4. Maintain hashmap of all orders 
        5. Maintain hashmap of all price levels for faster accessibility
        6. Maintain Total Volume on each side of the book
        7. Main min and max price levels of bid/ ask side of the book. This helps in getting the top of the book quickly
        
        """

        self.pricetree  = FastRBTree()
        self.priceMap   = {}  # map of price to its corresponding orderList
        self.orderMap   = {}  # map of each orderID with its order object

        self.minPrice = None
        self.maxPrice = None
        self.prevMinPrice = None
        self.prevMaxPrice = None

        self.volume = 0


    def __len__(self):
        # returns total orders on this side of the book (either Bid side or Ask side)
        return len(self.orderMap)
    
    def getPriceMap(self, price):
        # returns the orderList corresponding a particular price
        return self.priceMap[price]
    
    def getOrder_fromID(self, orderID):
        return self.orderMap[orderID]
    

    def createnewPrice(self, price):
        """
        adds a new Price node onto this tree
        """

        # create a new Order list
        orderlist = priceorderListManager.OrderList(price = price)

        # insert this price onto the tree
        self.pricetree.insert(price, orderlist)

        self.priceMap[price] = orderlist

        if self.maxPrice == None or price > self.maxPrice:
            self.maxPrice, self.prevMaxPrice = price, self.maxPrice
        if self.minPrice == None or price < self.minPrice:
            self.minPrice, self.prevMinPrice = price, self.minPrice        

        # # update the min and max price as needed
        # if self.minPrice is None and self.maxPrice is None:
        #     self.minPrice = price
        #     self.maxPrice = price
        # elif self.minPrice is None:
        #     if price > self.maxPrice:
        #         self.prevMaxPrice = self.maxPrice
        #         self.minPrice, self.maxPrice = self.maxPrice, price
        #     else:
        #         self.minPrice = price

        # elif self.maxPrice is None:
        #     if price < self.minPrice:
        #         self.prevMinPrice = self.minPrice
        #         self.minPrice, self.maxPrice = price, self.minPrice
        #     else:
        #         self.maxPrice = price


    def removePrice(self, price):
        """
        removes a price Node from the tree
        """

        self.pricetree.remove(price)
        del self.priceMap[price]

        if self.maxPrice == price:
            try:
                self.prevMaxPrice = self.maxPrice
                self.maxPrice = max(self.pricetree)
            except:
                self.maxPrice = None

        if self.minPrice == price:
            try:
                self.prevMinPrice = self.minPrice
                self.minPrice = min(self.pricetree)
            except:
                self.minPrice = None

    def checkPriceExists(self, price):
        return price in self.priceMap
    
    def checkOrderExists(self, orderID):
        return orderID in self.orderMap
    

    def processTick(self, tick):

        if tick.messageType == "N":
            # new Order
            self._insertnewTick(tick)

        elif tick.messageType == "M":
            # order modification
            self._updateOrder(tick)

        elif tick.messageType == "X":
            # order cancellation
            self._deleteOrder(tick)


    
    def _insertnewTick(self, tick):
        """
        tick: dtype: Tick (or its child)
        """

        if tick.price not in self.priceMap:
            self.createnewPrice(price = tick.price)
        
        # create a new order based on this tick
        order = orderManager.Order(tick=tick, order_list=self.priceMap[tick.price])

        # append this order onto the orderList
        self.priceMap[tick.price].append_order(order)

        # update the order map
        self.orderMap[order.orderID] = order
        self.volume += order.quantity


    def _updateOrder(self, tick):
        """
        updates the order based on the incoming tick        
        tick: dtype: Tick (or its child)
        """

        orderID = tick.orderID
        if orderID in self.orderMap:
            order = self.orderMap[orderID]
            oldPrice = order.price

            if tick.price == oldPrice:
                # No Price update
                if tick.qty != order.quantity:
                    # Quantity update
                    order.updateQty(newQty = tick.qty, newtimeStamp = tick.timestamp)
                    self.volume = self.volume + tick.qty - order.quantity

            else:
                # Price update
                if tick.price not in self.priceMap:
                    self.createnewPrice(price = tick.price)

                # update the order's old price list, i.e. remove this order from the old price map
                oldpriceMap = self.priceMap[oldPrice]
                oldpriceMap.delete_order(order)

                # delete the order from order map
                del self.orderMap[orderID]

                if oldpriceMap.nbOrders == 0:
                    self.removePrice(oldPrice)


                # update the new order
                priceMap = self.priceMap[tick.price]

                # create a new order to be added in this price map and add it in the price map
                newOrder = orderManager.Order(tick=tick, order_list=priceMap)
                priceMap.append_order(newOrder)
                self.orderMap[order.orderID] = newOrder
                
                self.volume = self.volume + tick.qty - order.quantity   

        else:
            # create a new order
            self._insertnewTick(tick)



            


    def _deleteOrder(self, tick):
        orderID = tick.orderID
        if orderID in self.orderMap:
            order = self.orderMap[orderID]

            # priceMap = self.priceMap[tick.price]
            if order.price in self.priceMap:
                # this if condition added as fall safe on 25 feb
                priceMap = self.priceMap[order.price]
                priceMap.delete_order(order)

                # if len(self.priceMap) == 0:
                if priceMap.volume == 0:
                    # remove the price, as there are no orders at this level
                    # self.removePrice(price = tick.price)
                    self.removePrice(price = order.price)

                self.volume -= order.quantity


    def max(self):
        return self.maxPrice
    
    def min(self):
        return self.minPrice



    

        




        





            


    



