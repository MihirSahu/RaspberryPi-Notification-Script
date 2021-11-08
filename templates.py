# Templates from https://support.pushover.net/i44-example-code-and-pushover-libraries#python

# Simple text notification
"""
import http.client, urllib

conn = http.client.HTTPSConnection("api.pushover.net:443")

conn.request("POST", "/1/messages.json",
  urllib.parse.urlencode({
    "token": "APP_TOKEN",
    "user": "USER_KEY",
    "message": "hello world",
  }), { "Content-type": "application/x-www-form-urlencoded" })

conn.getresponse()
"""

# Image attachment
"""
import requests
r = requests.post("https://api.pushover.net/1/messages.json", data = {
  "token": "APP_TOKEN",
  "user": "USER_KEY",
  "message": "hello world"
},
files = {
  "attachment": ("image.jpg", open("your_image.jpg", "rb"), "image/jpeg")
})
print(r.text)
"""
