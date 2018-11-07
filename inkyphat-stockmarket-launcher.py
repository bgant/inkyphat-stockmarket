#!/usr/bin/python3
#
# Brandon Gant
# Created: 2018-11-01
#
# This script makes sure crontab stock updates only happen when the market is open.
#
# /etc/crontab entry:
# */2 *   * * 1-5 pi      /home/pi/inkyphat-stockmarket/inkyphat-stockmarket-launcher.py &
#

import datetime
import os.path
import os

##########################################################
###  Customized user variables
##########################################################

dir     = "/home/pi/inkyphat-stockmarket/"
enable  = "crontab-enable"


##########################################################
###  Make sure Stock Market is open 
##########################################################

time    = int(datetime.datetime.now().strftime("%H%M"))
day     = int(datetime.datetime.now().strftime("%u"))   # The day of the week range 1 to 7 with Monday being 1

#time = 847  # Test Times
enable_check         = os.path.isfile(dir + enable)
market_open_check    = time >= 830
market_close_check   = time < 1500
weekend_check        = day <= 5

# Check if we have disabled crontab launcher for maintenance
if enable_check == False:
	print('crontab-enable file missing')
	exit()

# Markets are open 8:30AM to 3:00PM Central Time Monday through Friday
if weekend_check and market_open_check and market_close_check:
	print('Updating inky pHat...')
	os.system(dir + "inkyphat-stockmarket.py &")
else:
	print('Stock Market is currently closed')


#print("\n")
#print("        Time: ", time)
#print("     Enabled: ", enable_check)
#print("     Weekend: ", weekend_check)
#print("  After Open: ", market_open_check)
#print("Before Close: ", market_close_check)

