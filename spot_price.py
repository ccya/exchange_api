"""
A class to represent spot price for targeted pair from exchange.
This will be used as input to calculator.
"""
from datetime import datetime
from enum import Enum
class Pair(Enum):
    USDBTC = 1

class SpotPrice:
   exchange = ""
   timestamp = None
   pair = None
   price = None


   def __init__(self, exchange, timestamp, pair, price):
      self.exchange = exchange
      self.timestamp = timestamp
      self.pair = pair
      self.price = price