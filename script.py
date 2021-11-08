import http.client, urllib
import datetime
import time
import subprocess

# Used to save last check
lastCheck = datetime.datetime.now().minute

# Functions
def sendNotification(title, message):
	conn = http.client.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",

	  urllib.parse.urlencode({
	    "token": "",
	    "user": "",
	    "title": title,
	    "message": message,
	  }), { "Content-type": "application/x-www-form-urlencoded" })

	print(conn.getresponse().read())

async def sleepNotification():
	while True:
		if (datetime.datetime.now().hour == 23) and (datetime.datetime.now().minute == 59):
			await sendNotification("Go to sleep!", "It's 12:00! Go to sleep or you'll regret it tomorrow :p")
			await time.sleep(60 - datetime.datetime.now().second)
		else:
			await time.sleep((abs(datetime.datetime.now().hour - 23) * 60 * 60) + (abs(datetime.datetime.now().minute - 59) * 60) + (abs(datetime.datetime.now().second - 50)))

async def tempNotification():
	while True:
		if ((lastCheck + 10) % 60) == (datetime.datetime.now().minute):
			lastCheck = datetime.datetime.now().minute
			temp = str(subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True)).rstrip()
			if float(temp[(temp.find('=') + 1):(temp.find("'"))]) > 50:
				await sendNotification("High Temperature Warning", "Raspberry Pi temperature is over 50 degrees Celcius!")
		else:
			time.sleep(570)

# Run
await sleepNotification()
await tempNotification()
