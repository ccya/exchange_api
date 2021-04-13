import configs
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector


class MarketServer(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/index_price':
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			result = self.fetchPrice()
			if result is not None:
				data_set = {"index_price": result['index_price'], 'created_timestamp': result['timestamp'].strftime("%Y/%m/%d %H:%M:%S")}   
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