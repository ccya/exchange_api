"""
Define the interface for an exchange. This will be extended if new exchange get added to the system.

"""
from spot_price import SpotPrice
from abc import ABC, abstractmethod

class Parser(ABC):
	@abstractmethod
	def convertRequest(self): #TODO Pair enum
		pass

	@abstractmethod
	def convertResponse(self):
		pass