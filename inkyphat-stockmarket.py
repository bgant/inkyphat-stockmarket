#!/usr/bin/python3
#
# Brandon Gant
# created: 2018-10-30
#

import sys
from PIL import Image, ImageFont
import inkyphat
import datetime

# Move into the directory of this script 
import os.path
os.chdir(os.path.dirname(os.path.abspath(__file__))) 

##########################################################
###  Customized user variables
##########################################################

inkyphat.set_colour('red')
# 'red' is the three color (Black, White, Red) inky pHat.
# 'yellow' is the three color (Black, White, Yellow) inky pHat.
# 'black' is the original two color (Black, White) inky pHat.

# Common stock symbols:
#	^DJI  Dow Jones Industrial Average
#	SPX   S&P 500 Index
#	NYA   NASDAQ Composite Index
# Which stock symbol do you want to watch?
symbol = '^DJI'


##########################################################
###  Download the stock data (multiple options)
##########################################################

#import alphavantage
#quote = alphavantage.lookup(symbol)

import apple_finance
quote = apple_finance.lookup(symbol)


##########################################################
###  Manipulate the string data  
##########################################################

latest_trading_day = quote.day()

price = quote.price()
if len(str(price)) >= 8: 
    price = str(round(float(price)))      # Remove decimals on numbers larger than 9999
else:
    price = round(float(price),2)         # Round to two decimals on numbers less than 10000
    price = str("{:.2f}".format(price))   # Print trailing zeros after decimal if needed

change_percent = quote.percent()
change_percent = str(round(float(change_percent[:-1]), 1))    # Strip "%" sign, convert string to float, round to single decimal, convert back to string

if float(change_percent) < 0:
    text_colour = inkyphat.RED
    plus_sign = ""
else:
    text_colour = inkyphat.BLACK
    plus_sign = "+"

# Let's throw in some weather icons depending on the price change today
if float(change_percent) < -2:
    icon = "./images/icon-storm.png"
elif float(change_percent) < -1 :
    icon = "./images/icon-rain.png"
elif float(change_percent) < 0:
    icon = ""
elif float(change_percent) >= 2:
    icon = "./images/icon-sun.png"
else:
    icon = ""

change_percent = plus_sign + change_percent + "%"


##########################################################
###  Draw images on the inky pHat
##########################################################

inkyphat.set_border(text_colour)

price_font_size = 36
price_image_size = ImageFont.truetype(inkyphat.fonts.FredokaOne, price_font_size)
price_image_width, price_image_height = inkyphat.textsize(price, price_image_size)
price_image_x = (inkyphat.WIDTH / 2) - (price_image_width / 2)
price_image_y = 40 - (price_image_height / 2)
inkyphat.text((price_image_x, price_image_y), price, text_colour, price_image_size)

change_percent_font_size = 20
change_percent_image_size = ImageFont.truetype(inkyphat.fonts.FredokaOne, change_percent_font_size)
change_percent_image_width, change_percent_image_height = inkyphat.textsize(change_percent, change_percent_image_size)
change_percent_image_x = (inkyphat.WIDTH / 2) - (change_percent_image_width / 2)
change_percent_image_y = 70 - (change_percent_image_height / 2)
inkyphat.text((change_percent_image_x, change_percent_image_y), change_percent, text_colour, change_percent_image_size)

clock_font_size = 11
clock_image_size = ImageFont.truetype(inkyphat.fonts.FredokaOne, clock_font_size)
clock_image_x = 150   # Max 212
clock_image_y = 90    # Max 104
#time_stamp = str(datetime.datetime.now().strftime("%Y-%m-%d")) # Today's Date
time_stamp = latest_trading_day # Stock's Last Trading Day
inkyphat.text((clock_image_x, clock_image_y), time_stamp, inkyphat.BLACK, clock_image_size)

inkyphat.text((5, 5), symbol, inkyphat.BLACK, clock_image_size)

if len(icon) > 0:   # Check that png file is specified before trying to display it
    inkyphat.paste(Image.open(icon), (167, 5))

inkyphat.show()

