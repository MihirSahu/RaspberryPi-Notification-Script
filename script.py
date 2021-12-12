#!/usr/bin/python3

import http.client, urllib
import urllib.request
import datetime
import subprocess
import pandas

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

# Remind me to sleep between 12AM and 3AM. A flag.txt is used to ensure that it doesn't keep sending the message every 10 minutes
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

# Notify me if the raspberry pi temp gets too high. Logs temp and time on logs.txt
def tempNotification():
	temp = str(subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True)).rstrip()
	if float(temp[(temp.find('=') + 1):(temp.find("'"))]) > 50:
		sendNotification("High Temperature Warning", "Raspberry Pi temperature is over 50 degrees Celcius!")
		with open('logs.txt', 'a') as file:
			file.write(str(datetime.datetime.now()) + '\n')

# Downlads my to do list and sends me notifications based on the timing of the todo
def todoNotification():
        urllib.request.urlretrieve('https://docs.google.com/spreadsheets/d/e/2PACX-1vSk8th8flE8QIZ8avwQCyMVTLjZU0wH2dLrVzsKualattHEMT6bBIOWcMOiCAZMJqCyDYjbQeRVA-Uf/pub?output=xlsx', 'To-Do.xlsx')
        file = pandas.read_excel('To-Do.xlsx')

        for idx, date in enumerate(list(file["Date"])):
                if date.date().strftime("%Y-%m-%d") == datetime.datetime.now().strftime("%Y-%m-%d"):
                        time = list(file["Time"])[idx]
                        if (time.hour <= datetime.datetime.now().hour) and (time.minute < datetime.datetime.now().minute):
                                if (((datetime.datetime.now().hour - time,hour)*60) + (datetime.datetime.now().minute - time.minute)) < 30:
                                        sendNotification(list(file["To-Do"])[idx])

# Run
sleepNotification()
tempNotification()
todoNotification()
