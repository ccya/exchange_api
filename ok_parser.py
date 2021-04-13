import base64
import datetime
import dateutil.parser as dp
import hmac
import json
from parser import Parser
from spot_price import SpotPrice
import zlib

class OkParser(Parser):

	# override function
	def getUrl(self):
		return "wss://real.okex.com:8443/ws/v3"

	# override function
	def convertRequest(self):
		request_str = "spot/ticker:BTC-USDT"
		param = {"op": "subscribe", "args": [request_str]}
		return json.dumps(param)

	# override function
	def convertResponse(self, message):
		response_str = self.inflate(message).decode('utf-8')
		# print("ok resp: " + response_str)
		response = eval(response_str)
		if ('data' not in response):
			return None
		return SpotPrice("OK",response['data'][0]['timestamp'],"BTC-USDT",float(response['data'][0]['last']))


	def inflate(self, data):
		decompress = zlib.decompressobj(
				-zlib.MAX_WBITS  # see above
		)
		inflated = decompress.decompress(data)
		inflated += decompress.flush()
		return inflated
