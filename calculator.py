"""
The calculator for index_price. 
Input is a list of SpotPrice and output is the final index_price. 
The result will be saved to database / memory
"""
import asyncio
import configs
import datetime
from database import DbHelper
from parser_binance import BinanceParser
from parser_huobi import HuobiParser
from parser_ok import OkParser
import statistics

class Calculator():
	def __init__(self):
		self.parsers = [BinanceParser(), OkParser(), HuobiParser()]
		self.last_sigma = None
		self.last_mean = None
		self.spot_prices = None
		# past prices used to filter noise. ordered by time in desc order.
		self.past_price = [] 
		self.prod_mode = True
		self.dbHelper = DbHelper()

	def fetchSpotPrice(self, loop):
		asyncio.set_event_loop(loop)
		for parser in self.parsers:
			asyncio.ensure_future(parser.run())
		loop.run_forever()

	def fetchPrevious(self):
		query_str= "SELECT index_price, sigma, mean from index_price where timestamp >= DATE_SUB(NOW(), INTERVAL 5 MINUTE) order by timestamp desc;"
		result = self.dbHelper.fetch(query_str)
		if result is None or len(result) == 0:
			return
		self.last_sigma = result[0]['sigma']
		self.last_mean = result[0]['mean']
		for row in result:
			self.past_price.append(row['index_price'])

	def filter(self, current_price):
		if (len(self.past_price) == 0) and self.last_sigma is None and self.last_mean is None:
			return(current_price, 0.0, current_price, True)
		current_sigma = statistics.pstdev(self.past_price+[current_price])
		current_mean = statistics.mean(self.past_price+[current_price])
		# If current_price is in of 3 sigma based on past_price,
		# store the price as valid.
		if current_price >= self.last_mean - 3 * self.last_sigma and current_price <= self.last_mean + 3 * self.last_sigma:
			return(current_price, current_sigma, current_mean, True)
		else:
			# if current price is out 3 sigma (the sigma for past 5 minutes price) range, 
			# do not return it, only record the price and the new sigma.
			return (current_price, current_sigma, current_mean, False)

	def calculate(self):
		current_price = 0
		# read data from parser. If test mode, the spot_price will be prepared.
		if self.prod_mode:
			self.spot_prices = []
			for parser in self.parsers:
				if parser.spot_price is None:
					# print("[Calculator]Warning: No result fetched from Websocket yet")
					return None
				if parser.getWeight() is None:
					# if no special weight returned, means this is "equal weight stragety"
					self.spot_prices.append((parser.spot_price.price)*1.0000/len(self.parsers))
				else:
					self.spot_prices.append((parser.spot_price.price)*1.0000 * parser.getWeight())

		current_price = sum(self.spot_prices)
		index, sigma, mean, valid = self.filter(current_price)
		return (index, sigma, mean, valid)

	def saveToDb(self, result):
		sql_str = "INSERT INTO index_price (timestamp, index_price, sigma, mean, valid) VALUES (%s, %s, %s, %s, %s)"
		val = (datetime.datetime.now() , result[0], result[1], result[2], result[3])
		self.dbHelper.mutate(sql_str, val)


	def close(self, loop):
		if loop.is_running():
			for parser in self.parsers:
				parser.close()
			loop.close()
		else:
			print("[Calculator]Warning: No running loop to close")






		
