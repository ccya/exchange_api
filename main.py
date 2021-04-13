"""
Create two threads. One for pulling index_price for api; one to run in background
to write the newest index_price to the database / memory.

"""
import asyncio
from calculator import Calculator
import configs
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector
from threading import Thread
import time


def setupDB():
	mydb = mysql.connector.connect(
		host = configs.HOST,
		user = configs.USER,
		password = configs.PASSWORD,
		auth_plugin='mysql_native_password')
	mycursor = mydb.cursor()
	mycursor.execute("CREATE DATABASE IF NOT EXISTS exchange_api;")
	mycursor.execute("USE exchange_api;")
	mycursor.execute("""CREATE TABLE IF NOT EXISTS index_price (
							id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
							timestamp TIMESTAMP, 
							index_price FLOAT(20,7),
							mean FLOAT(10,3),
							sigma FLOAT(10,3));""")

def fetchIndex(calculator, loop):
	calculator.fetchSpotPrice(loop);

def calculateIndex(calculator):
	while True:
		try:
			result = calculator.calculate()
			if result is not None:
				calculator.saveToDb(result)
			time.sleep(5)
		except KeyboardInterrupt:
			calculator.close(loop)
			break

class MarketServer(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/index_price':
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			result = self.fetchPrice()
			if result is not None:
				data_set = {"index_price": result['index_price'], 'created_timestamp': datetime.timestamp(result['timestamp'])}   
				self.wfile.write(bytes(json.dumps(data_set), "utf-8"))
			else:
				self.wfile.write(bytes("No data yet, please refresh after few seconds", "utf-8"))
		else:
			self.wfile.write(bytes("only support path /index_price", "utf-8"))
	def fetchPrice(self):
		mydb = mysql.connector.connect(
		host = configs.HOST,
		user = configs.USER,
		password = configs.PASSWORD,
		database=configs.DATABASE,
		auth_plugin='mysql_native_password')
		mycursor = mydb.cursor(dictionary = True)
		mycursor.execute("SELECT index_price, timestamp from index_price order by id desc limit 1;")
		result = mycursor.fetchone()
		mydb.close()
		return result

def startServer():
	webServer = HTTPServer((configs.SERVER_HOST, configs.SERVER_PORT), MarketServer)
	print("Server started http://%s:%s" % (configs.SERVER_HOST, configs.SERVER_PORT))
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass
	webServer.server_close()
	print("Server stopped.")

if __name__ == '__main__':
	setupDB()
	loop = asyncio.new_event_loop()
	calculator = Calculator()
	T1 = Thread(target=startServer, args=())
	T1.start()
	T2 = Thread(target=fetchIndex, args=(calculator, loop, ))
	T2.start()
	T3 = Thread(target=calculateIndex, args=(calculator, ))
	T3.start()

