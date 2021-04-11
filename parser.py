"""
Define the interface for an exchange. This will be extended if new exchange get added to the system.

"""

from abc import ABC, abstractmethod
import asyncio
import websockets

class Parser(ABC):
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
		ws = await websockets.connect(url)
		await ws.send(request_str)
		while True:
			try:
				response_byte = await ws.recv()
				spot_price = self.convertResponse(response_byte)
				if spot_price is not None: 
					await ws.close()
					return spot_price
				# continue wait for a valid message
			except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosedError) as e:
				try:
					await ws.send('ping')
					ping_response_byte = await ws.recv()
					 # continue waiting for the response if pinged successfully
					continue
				except Exception as e:
					print("error in receiving msg")
					# if ping failed, stop waiting for the message for this connection
					break
