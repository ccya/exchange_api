"""
The calculator for index_price. 
Input is a list of SpotPrice and output is the final index_price. 
The result will be saved to database / memory
"""

from ok_parser import OkParser

class Calculator():

	def calculate(self):
		ok_parser = OkParser()
		ok_parser.convertRequest() # Pass pair enum here
		ok_spot = ok_parser.convertResponse()
		return ok_spot.price
		
