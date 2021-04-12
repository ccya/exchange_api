"""
Create two threads. One for pulling index_price for api; one to run in background
to write the newest index_price to the database / memory.

"""
from calculator import Calculator
import configs
import mysql.connector

def createDB():
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

def main():
	# TODO: For every 5 second, do a calculation
	print("TODO: THE 5 SECOND THING")
	calculator = Calculator()
	calculator.fetchSpotPrice();
	calculator.fetchPrevious()	
	result = calculator.calculate()
	calculator.saveToDb(result[0], result[1])

	

if __name__ == '__main__':
	createDB()
	main()