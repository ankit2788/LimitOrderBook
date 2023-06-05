# LimitOrderBook
Create LOB using TBT Data (Indian Markets)

**Important Considerations**

1. Need to maintain Price time priority
2. Three main operations:
    * Inserting a new order into the book. 
    * Search/ Delete an order into the book
    * Execute an order, i.e. Process an order

    Here are the time complexities 
    * Add – O(log M) for the first order at a limit price, O(1) for all others
        Reason: for 1st order at a price, need to insert a new price level. This takes O(log m) in a Binary Tree
                for other orders, since we are preparing a hashmap for all price levels, and its corresponding order list, its O(1)
    * Cancel – O(1)
        Reason:
            Search in a hashmap --> O(1)
            Then delete from hashmap --> O(1)

    * Execute – O(1)
    * GetVolumeAtLimit – O(1)        
    * GetBestBid/Offer – O(1)


## HOW TO RUN
use Python script: bookCreator.py to create the LOB book
(NOTE: update the script for the relevant TBT data file)
