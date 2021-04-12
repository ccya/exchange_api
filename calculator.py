"""
The calculator for index_price. 
Input is a list of SpotPrice and output is the final index_price. 
The result will be saved to database / memory
"""
import asyncio
import configs
import datetime
import mysql.connector
from ok_parser import OkParser
from binance_parser import BinanceParser
from huobi_parser import HuobiParser
import statistics

class Calculator():
	def __init__(self):
		self.parsers = [
		# OkParser(),
		# BinanceParser(),
		HuobiParser()
		]
		self.spot_prices = []
		self.last_sigma = None
		self.last_mean = None
		# past prices used to filter noise. ordered by time desc.
		self.past_price = [] 

	def fetchSpotPrice(self):
		loop = asyncio.get_event_loop()
		for parser in self.parsers:
			self.spot_prices.append(loop.run_until_complete(parser.run()))

	def fetchPrevious(self):
		mydb = mysql.connector.connect(
			host = configs.HOST,
			user = configs.USER,
			password = configs.PASSWORD,
			auth_plugin='mysql_native_password',
			database=configs.DATABASE);
		mycursor = mydb.cursor(dictionary = True)
		query_str= "SELECT index_price, sigma, mean from index_price where timestamp BETWEEN NOW() and NOW() - INTERVAL 5 MINUTE order by timestamp desc"
		# value = (datetime.datetime.now() - datetime.timedelta(minutes=5))
		mycursor.execute(query_str)
		result = mycursor.fetchall()
		for row in result:
			if result is None:
				mydb.close()
				return
			self.past_price.append(result['index_price'])
			self.last_sigma = result['sigma']
			self.last_mean = result['mean']
		mydb.close()


	def filter(self, current_price):
		if (len(self.past_price) == 0) and self.last_sigma is None and self.last_mean is None:
			return(current_price, 0.0, current_price)
		# If current_price is in of 3 sigma based on past_price,
		# store the price, calculate the sigma of last 5 min price and store it.
		if current_price >= self.last_mean - 3 * self.last_sigma and current_price <= self.last_mean + 3 * self.last_sigma:
			current_sigma = statistics.pstdev(self.past_price+[current_price])
			current_mean = statistics.mean(self.past_price+[current_price])
			return(current_price, current_sigma, current_mean)
		else:
			# check if majority of original data is inside the 3 sigma range, if so consider there are bad data.
			# Use those data in range to calculate current_price and new sigma
			valid_count = 0
			in_range_price = []
			for spot in self.spot_prices:
				if spot.price >= self.last_mean - 3 * self.last_sigma and spot.price <= self.last_mean + 3 * self.last_sigma:
					valid_count +=1
					in_range_price.append(spot.price)
			if valid_count >= (len(self.spot_prices)/2):
				current_price = (sum(in_range_price)*1.0000)/len(in_range_price)
				current_sigma = statistics.pstdev(self.past_price+[current_price])
				current_mean = statistics.mean(self.past_price+[current_price])
				return(current_price, current_sigma, current_mean)
			else:
				# If majority data is outside the 3 sigma range, consider there is a huge price change.
				# store the price and sigma
				current_sigma = statistics.pstdev(self.past_price+[current_price])
				current_mean = statistics.mean(self.past_price+[current_price])
				return(current_price, current_sigma, current_mean)

	def calculate(self):
		current_price = 0
		for price in self.spot_prices:
			current_price += price.price
		current_price = (current_price*1.0000)/len(self.spot_prices)
		index, sigma, mean = self.filter(current_price)
		print(index)
		print(sigma)
		print(mean)
		return (index, sigma, mean)

	def saveToDb(self, result):
		mydb = mysql.connector.connect(
			host = "localhost",
			user = "root",
			password = "password",
			auth_plugin='mysql_native_password',
			database="exchange_api");
		mycursor = mydb.cursor()
		sql_str = "INSERT INTO index_price (timestamp, index_price, sigma, mean) VALUES (%s, %s, %s, %s)"
		val = (datetime.datetime.now() , result[0], result[1], result[2])
		mycursor.execute(sql_str, val)
		mydb.commit()
		mydb.close()






		
