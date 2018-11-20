#!/usr/bin/python3
#
# Brandon Gant
# Created: 2018-11-01
#
# This script makes sure crontab stock updates only happen when the market is open.
#
# /etc/crontab entry:
# */5 *   * * 1-5 pi      /home/pi/inkyphat-stockmarket/inkyphat-stockmarket-launcher.py &
#

import os
from datetime import datetime
import pytz   # Python Timezones Module

base_dir = '/home/pi/inkyphat-stockmarket'

##########################################################
###  Is this script currently enabled?
##########################################################

# Check if we have disabled crontab launcher for maintenance
enable_check = os.path.isfile(base_dir + '/crontab-enable')
if enable_check == False:
    print('Launcher is currently disabled... Exiting')
    exit()


##########################################################
###  Is the Stock Market open? 
##########################################################
#
# List of Stock Exchange Trading Hours:
#   https://en.wikipedia.org/wiki/List_of_stock_exchange_trading_hours
#
# The United States New York Stock Exchange and NASDAQ are in the Eastern Time Zone.
# They are open from 9:30 to 16:00 and follow Daylight Savings Time.
#
# We'll let /etc/crontab make sure we are only running Monday through Friday.
#

# Instead of creating a multi-line "function", we can do the same thing with a single-line "lamba"
isDST_now_in = lambda zonename: bool(datetime.now(pytz.timezone(zonename)).dst())

# Are we currently in Daylight Savings or not?
if isDST_now_in('America/New_York') == False:
   # Eastern Standard Time (EST) is UTC -05:00 (markets open 14:30 to 21:00 UTC)
   market_open  = 1430 
   market_close = 2100
else:
   # Eastern Daylight Time (EDT) is UTC -04:00 (markets open 15:30 to 22:00 UTC)
   market_open  = 1530
   market_close = 2200

# Markets are closed all day on Saturday and Sunday
day_of_the_week = int(datetime.utcnow().strftime("%u"))   # The day of the week range 1 to 7 with Monday being 1

# Current hour and minute as an integer
time_now = int(str(datetime.utcnow().hour) + str(datetime.utcnow().minute))


##########################################################
### If the Stock Market is Open, run the main script
##########################################################

if market_open < time_now < market_close and day_of_the_week <= 5:
    print('Updating inky pHat...')
    os.system(base_dir + "/inkyphat-stockmarket.py &")
else:
    print('Stock Market is currently closed')


#print('Current Time: ', time_now)
#print('Day of Week:  ', day_of_the_week)
