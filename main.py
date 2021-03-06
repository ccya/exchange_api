"""
Create two threads. One for pulling index_price for api; one to run in background
to write the newest index_price to the database / memory.

"""
import asyncio
from calculator import Calculator
import configs
from database import DbHelper
from http.server import BaseHTTPRequestHandler, HTTPServer
from server import MarketServer
from threading import Thread
import time


def setupDB():
	dbHelper = DbHelper()
	sql_strs = ["CREATE DATABASE IF NOT EXISTS exchange_api;", "USE exchange_api;", 
	"""CREATE TABLE IF NOT EXISTS index_price (
		id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
		timestamp TIMESTAMP, 
		index_price FLOAT(20,7),
		mean FLOAT(10,3),
		sigma FLOAT(10,3),
		valid boolean);"""]
	dbHelper.create(sql_strs)

def calculateIndex(calculator):
	while True:
		try:
			calculator.fetchPrevious()
			result = calculator.calculate()
			if result is not None:
				calculator.saveToDb(result)
			time.sleep(5)
		except KeyboardInterrupt:
			calculator.close(loop)
			break

def startServer():
	webServer = HTTPServer((configs.SERVER_HOST, configs.SERVER_PORT), MarketServer)
	print("Server started http://%s:%s" % (configs.SERVER_HOST, configs.SERVER_PORT))
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		webServer.server_close()
		print("Server stopped.")

if __name__ == '__main__':
	setupDB()
	loop = asyncio.new_event_loop()
	calculator = Calculator()
	T1 = Thread(target=startServer, args=())
	T1.start()
	T2 = Thread(target=calculator.fetchSpotPrice, args=(loop, ))
	T2.start()
	T3 = Thread(target=calculateIndex, args=(calculator, ))
	T3.start()

