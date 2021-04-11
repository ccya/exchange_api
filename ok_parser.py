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
		print("resp: " + response_str)
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

	# def getTimestamp(self):
	# 	now = datetime.datetime.now()
	# 	t = now.isoformat("T", "milliseconds")
	# 	return t + "Z"

	# async def getPrice(self):
	# 	self.convertRequest()
	# 	while True:
	# 		try:	
	# 			async with websockets.connect(self.url) as ws:
	# 				await ws.send(self.request)
	# 			while True:
	# 				try:
	# 					response_byte = await asyncio.wait_for(ws.recv(), timeout=25)
	# 				except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
	# 					try:
	# 						await ws.send('ping')
	# 						ping_response_byte = await ws.recv()
	# 						timestamp = self.getTimestamp()
	# 						ping_res = self.inflate(ping_response_byte).decode('utf-8')
	# 						# print(timestamp + ping_res)
	# 						continue # continue waiting for the response if pinged successfully
	# 					except Exception as e:
	# 						print("error in receiving msg")
	# 						break

	# 				timestamp = self.getTimestamp()
	# 				response = self.inflate(response_byte).decode('utf-8')
	# 				self.convertResponse(response)
	# 				print("debug: " + response)
	# 		except Exception as e:
	# 			continue # continue to create websocket until success.
