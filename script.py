#!/usr/bin/python3

import http.client, urllib
import urllib.request
import datetime
import subprocess
import pandas
import multiprocessing

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

# Remind me to sleep between 12AM and 3AM
def sleepNotification():
	if (datetime.datetime.now().hour >= 0) and (datetime.datetime.now().hour <= 3):
		sendNotification("Go to sleep!", "Go to sleep or you'll regret it tomorrow :p")

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
                if list(file["Completion"])[idx] == "N":
                        if date.date().strftime("%Y-%m-%d") == datetime.datetime.now().strftime("%Y-%m-%d"):
                                #print("Same date")
                                timeDue = list(file["Time Due"])[idx]
                                notifyTime = list(file["Notification Time"])[idx]
                                if (datetime.datetime.now().hour >= notifyTime.hour) and (datetime.datetime.now().hour <= timeDue.hour):
                                        #print("Same time")
                                        comment = list(file["Comment"])[idx]
                                        sendNotification(list(file["To-Do"])[idx], comment + f' Due at {timeDue.strftime("%I:%M")}')
                                        '''
                                        if (((time.hour - datetime.datetime.now().hour)*60) + (time.minute - datetime.datetime.now().minute)) <= 60:
                                                sendNotification(list(file["To-Do"])[idx], "Testing")
                                                #print("Message sent")
                                        '''
                                elif (datetime.datetime.now().hour >= notifyTime.hour) and (timeDue.hour == 0) and (datetime.datetime.now().hour <= 24):
                                        comment = list(file["Comment"])[idx]
                                        sendNotification(list(file["To-Do"])[idx], comment + f' Due at {timeDue.strftime("%I:%M")}')

def main():
        sleepNotification()
        tempNotification()
        todoNotification()


# Run program and kill it if it takes longer than 60 seconds
p = multiprocessing.Process(target=main, name=mainScript)
time.sleep(60)
p.terminate()
p.join()
