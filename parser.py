"""
Define the interface for an exchange. This will be extended if new exchange get added to the system.

"""

from abc import ABC, abstractmethod
import asyncio
import websockets


class Parser(ABC):

	def __init__(self):
		self.spot_price = None
		self.ws = None
		self.connected = False

	@abstractmethod
	def getUrl(self):
		pass

	@abstractmethod
	def convertRequest(self):
		pass

	@abstractmethod
	def convertResponse(self, message):
		pass

	# return a SpotPrice object
	async def run(self):
		request_str = self.convertRequest();
		url = self.getUrl()
		response_byte = ""
		self.ws = await websockets.connect(url)
		self.connected = True
		if request_str is not None:
			await self.ws.send(request_str)
		while True:
			try:
				response_byte = await self.ws.recv()
				spot_price = self.convertResponse(response_byte)
				# print(spot_price)
				if spot_price is not None: 
					self.spot_price = spot_price
				# continue wait for a valid message
			except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
				try:
					await self.ws.send('ping')
					ping_response_byte = await self.ws.recv()
					 # continue waiting for the response if pinged successfully
					continue
				except Exception as e:
					print("[Parser] error in receiving msg")
					self.connected = False
					# if ping failed, stop waiting for the message for this connection
					break

	def close(self, ws):
		if self.connected and self.ws is not None:
			self.ws.close()
		else:
			print("[Parser] No active connection to close")