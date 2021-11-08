import http.client, urllib
import datetime
import time

conn = http.client.HTTPSConnection("api.pushover.net:443")

lastCheck = datetime.datetime.now().minute

while True:
	# Testing
	#print(str(lastCheck) + " " + str((datetime.datetime.now().minute + 1) % 60))

	"""
	if datetime.datetime.now().minute == (lastCheck + 5) % 60:
		conn.request("POST", "/1/messages.json",
		
		  urllib.parse.urlencode({
		    "token": "",
		    "user": "",
		    "title": "Testing",
		    "message": f"The minute is {datetime.datetime.now().minute}",
		  }), { "Content-type": "application/x-www-form-urlencoded" })
		
		print(conn.getresponse().read())

		lastCheck = (lastCheck + 1) % 60
	"""

	if (datetime.datetime.now().hour == 23) and (datetime.datetime.now().minute == 59):
		conn.request("POST", "/1/messages.json",
		
		  urllib.parse.urlencode({
		    "token": "",
		    "user": "",
		    "title": "Go to sleep!",
		    "message": f"It's 12:00! Go to sleep or you'll regret it :p",
		  }), { "Content-type": "application/x-www-form-urlencoded" })
		
		print(conn.getresponse().read())
		time.sleep(60 - datetime.datetime.now().second)
	else:
		time.sleep((abs(datetime.datetime.now().hour - 23) * 60 * 60) + (abs(datetime.datetime.now().minute - 59) * 60) + (abs(datetime.datetime.now().second - 50)))
