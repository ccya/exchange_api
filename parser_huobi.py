import gzip
import json
from parser import Parser
from spot_price import SpotPrice

class HuobiParser(Parser):

	# override function
	def getUrl(self):
		return "wss://api.huobi.pro/ws"

	# override function
	def convertRequest(self):
		param = {"sub": "market.btcusdt.detail", "id": "id1"}
		return json.dumps(param)

	# override function
	def convertResponse(self, message):
		response_str = gzip.decompress(message).decode()
		# print("huobi resp: " + response_str)
		response = eval(response_str)
		if ('tick' not in response):
			return None
		return SpotPrice("HUOBI",response['ts'],"BTC-USDT",float(response['tick']['close']))

