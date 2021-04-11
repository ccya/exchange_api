"""
The calculator for index_price. 
Input is a list of SpotPrice and output is the final index_price. 
The result will be saved to database / memory
"""
import asyncio
from ok_parser import OkParser

class Calculator():

	def calculate(self):
		loop = asyncio.get_event_loop()
		ok_parser = OkParser()
		ok_spot = loop.run_until_complete(ok_parser.run())# Pass pair enum here
		print(ok_spot.price)
		return ok_spot
		
