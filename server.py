import configs
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from database import DbHelper


class MarketServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.dbHelper = DbHelper()
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
		sql_str = "SELECT index_price, timestamp from index_price where valid order by id desc limit 1;"
		result = self.dbHelper.fetch(sql_str)
		if (len(result) > 0):
			return result[0]
