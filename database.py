import configs
import mysql.connector

class DbHelper:

	def __init__(self):
		self.host = configs.HOST
		self.user = configs.USER
		self.password = configs.PASSWORD
		self.database= configs.DATABASE

	def __connect__(self):
		self.con = mysql.connector.connect(
			host = self.host,
			user = self.user,
			password = self.password,
			auth_plugin='mysql_native_password',
			database=self.database);
		self.cur = self.con.cursor(dictionary = True)

	def __disconnect__(self):
		self.con.close()

	def create(self, sql_strs):
		self.__connect__()
		for sql in sql_strs:
			self.cur.execute(sql)
		self.__disconnect__()

	def fetch(self, sql_str):
		self.__connect__()
		self.cur.execute(sql_str)
		result = self.cur.fetchall()
		self.__disconnect__()
		return result

	def mutate(self, sql_str, new_value):
		self.__connect__()
		self.cur.execute(sql_str, new_value)
		self.con.commit()
		self.__disconnect__()
