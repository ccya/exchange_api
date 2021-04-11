from parser import Parser
from spot_price import SpotPrice

class OkParser(Parser):
	def convertRequest(self):
		print("Ok Req Convert")

	def convertResponse(self):
		print("Ok Resp Convert")
		return SpotPrice("ok",123,1,1)