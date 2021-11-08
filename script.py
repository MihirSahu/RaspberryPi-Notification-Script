import http.client, urllib
import datetime

conn = http.client.HTTPSConnection("api.pushover.net:443")

lastCheck = datetime.datetime.now().minute

while True:
	#print(str(lastCheck) + " " + str((datetime.datetime.now().minute + 1) % 60))
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
