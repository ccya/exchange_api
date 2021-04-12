"""
The calculator for index_price. 
Input is a list of SpotPrice and output is the final index_price. 
The result will be saved to database / memory
"""
import asyncio
import configs
from datetime import datetime
import mysql.connector
from ok_parser import OkParser


class Calculator():
	def __init__(self):
		self.parsers = [OkParser()
		# ,BinanceParser(), HuobiParser()
		]
		self.spot_prices = []
		self.last_price = None
		self.last_sigma = None

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
		mycursor.execute("SELECT index_price, sigma from index_price order by id desc limit 1;")
		result = mycursor.fetchone()
		if result is None:
			mydb.close()
			return
		mydb.close()
		self.last_price = result['price']
		self.last_sigma = result['sigma']


	def filter(self, current_price):
		if self.last_price is None and self.last_sigma is None:
			print("TODO CALCULATE SIGMA")
			return(current_price, 1.1)
		# If current_price is in of 3 sigma based on last_price,
		# store the price, calculate the sigma of last 5 min price and store it.
		if current_price in range(self.last_price - 3 * self.last_sigma,self.last_price + 3 * self.last_sigma):
			print("TODO CALCULATE SIGMA")
			return(current_price, 1.1)
		else:
			# check if majority of original data is inside the 3 sigma range, if so consider there are bad data.
			# Use those data in range to calculate current_price and new sigma
			valid_count = 0
			for spot in self.spot_prices:
				if spot.price in range(self.last_price - 3 * self.last_sigma,self.last_price + 3 * self.last_sigma):
					valid_count +=1
			if valid_count >= len(self.spot_prices)/2+1:
				print("TODO NOISE DATA")
				return(1.2, 1.1)
			else:
				# If majority data is outside the 3 sigma range, consider there is a huge price change.
				# store the price and sigma
				print("TODO CALCULATE SIGMA")
				return(current_price, 1.1)

	def calculate(self):
		self.fetchSpotPrice();
		self.fetchPrevious()
		current_price = 0
		for price in self.spot_prices:
			current_price += price.price
		current_price = (current_price*1.0)/len(self.spot_prices)
		index, sigma = self.filter(current_price)
		print(index)
		print(sigma)
		self.saveToDb(index, sigma)

	def saveToDb(self, price, sigma):
		mydb = mysql.connector.connect(
			host = "localhost",
			user = "root",
			password = "password",
			auth_plugin='mysql_native_password',
			database="exchange_api");
		mycursor = mydb.cursor()
		sql_str = "INSERT INTO index_price (timestamp, index_price, sigma) VALUES (%s, %s, %s)"
		val = (datetime.now() , price, sigma)
		mycursor.execute(sql_str, val)
		mydb.commit()
		mydb.close()






		
