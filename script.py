#!/usr/bin/python3

import http.client, urllib
import datetime
import subprocess

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

def sleepNotification():
	with open('flag.txt', 'r') as file:
		sentMessage = file.readline().strip()
		if sentMessage == "False":
			if (datetime.datetime.now().hour >= 0) and (datetime.datetime.now().hour <= 3):
				sendNotification("Go to sleep!", "Go to sleep or you'll regret it tomorrow :p")
				with open('flag.txt', 'w') as file:
					file.write("True")
			else:
				with open('flag.txt', 'w') as file:
					file.write("False")

def tempNotification():
	temp = str(subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True)).rstrip()
	if float(temp[(temp.find('=') + 1):(temp.find("'"))]) > 50:
		sendNotification("High Temperature Warning", "Raspberry Pi temperature is over 50 degrees Celcius!")
		with open('logs.txt', 'a') as file:
			file.write(str(datetime.datetime.now()) + '\n')

# Run
sleepNotification()
tempNotification()
