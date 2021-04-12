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
		response = eval(message)
		print(response)
		if ('c' not in response):
			return None
		return SpotPrice("BINANCE",response['E'],"BTC-USDT",float(response['c']))

