import json
from parser import Parser
from spot_price import SpotPrice

class BinanceParser(Parser):

	# override function
	def getUrl(self):
		return "wss://stream.binance.com:9443" + "/ws/btcusdt@miniTicker"

	# override function
	def convertRequest(self):
		return None

	# override function
	def convertResponse(self, message):
		# print("binance " + message)
		response = eval(message)
		if ('c' not in response):
			return None
		result = SpotPrice("BINANCE",response['E'],"BTC-USDT",float(response['c']))
		return result
