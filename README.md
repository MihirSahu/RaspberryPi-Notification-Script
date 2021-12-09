# Raspberry Pi Phone Notification Script

This script allows me to send notifications to my phone through the [Pushover](https://www.pushover.net) service whenever an event occurs.

## Setup
1. Create an account on Pushover (a one time purchase of $5 is required)
2. Replace token and user with Pushover application token and user token
3. Set the script as an executable `chmod +x script.py`
4. Create a cron job with crontab to run the script
    - Run `crontab -e` to get into crontab editor
    - Enter `*/10 * * * * path/to/script/script.py` on a new line. This will make the script run every 10 minutes
