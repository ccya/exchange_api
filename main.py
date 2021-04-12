"""
Create two threads. One for pulling index_price for api; one to run in background
to write the newest index_price to the database / memory.

"""
from calculator import Calculator
import configs
import mysql.connector
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime


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

def calcuateIndex():
	# TODO: For every 5 second, do a calculation
	print("TODO: THE 5 SECOND THING")
	calculator = Calculator()
	calculator.fetchSpotPrice();
	calculator.fetchPrevious()	
	result = calculator.calculate()
	calculator.saveToDb(result)

class MarketServer(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/index_price':
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			result = self.fetchPrice()
			print(result)
			data_set = {"index_price": result['index_price'], 'created_timestamp': datetime.timestamp(result['timestamp'])}   
			self.wfile.write(bytes(json.dumps(data_set), "utf-8"))
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



if __name__ == '__main__':
	# setupDB()
	# print("TODO the threading thing")
	# calcuateIndex()
	print("TODO the threading thing")
	webServer = HTTPServer((configs.SERVER_HOST, configs.SERVER_PORT), MarketServer)
	print("Server started http://%s:%s" % (configs.SERVER_HOST, configs.SERVER_PORT))
	try:
		webServer.serve_forever()
	except KeyboardInterrupt:
		pass

	webServer.server_close()
	print("Server stopped.")
