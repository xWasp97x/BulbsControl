import urequests


class ConnectionTester:
	def ping(self):
		try:
			response = urequests.get("http://clients3.google.com/generate_204")
			return response.status_code
		except:
			return 300

	def isConnected(self):
		if 200 <= self.ping() < 300:
			return True
		else:
			return False
