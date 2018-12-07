#!/usr/bin/python3
#
# Brandon Gant
# created: 2018-10-30
#

import os
import inkyphat
from PIL import Image, ImageFont

# Move into the directory of this script 
base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)


##########################################################
###  Read Values from the configuration ini file
##########################################################
import configparser
config = configparser.ConfigParser()
if os.path.exists('inkyphat-stockmarket.ini'):
    config.read('inkyphat-stockmarket.ini')
else:
    print("Creating inkyphat-stockmarket.ini file... Edit file to add API key and change script parameters")
    import shutil
    shutil.copyfile(base_dir + '/packages/inkyphat-stockmarket.ini.sample', base_dir + '/inkyphat-stockmarket.ini')
    exit()
symbol         = config.get('inkyphat_stockmarket', 'symbol')
exchange_name  = config.get('inkyphat_stockmarket', 'exchange_name')
inky_type      = config.get('inkyphat_stockmarket', 'inky_type')
inky_color     = config.get('inkyphat_stockmarket', 'inky_color')
crontab        = config.get('inkyphat_stockmarket', 'crontab')


##########################################################
###  If crontab is enabled, is the Exchange open now?
##########################################################
if crontab == 'enabled':
    import packages.stockmarket
    exchange_open = packages.stockmarket.exchange(exchange_name).hours() 
    if exchange_open == False:
        print('crontab enabled:', exchange_name.upper(), 'exchange is currently closed... Exiting')
        exit()
    else:
        print('crontab enabled:', exchange_name.upper(), 'exchange is currently open... Updating Inky display')
else:
    print('crontab disabled: Manually updating Inky display')


##########################################################
###  Download the stock data (multiple options)
##########################################################

import packages.alphavantage
quote = packages.alphavantage.lookup(symbol)

#import packages.apple_finance
#quote = packages.apple_finance.lookup(symbol)


##########################################################
###  Manipulate the string data for Inky display 
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
    plus_sign = "" # number already has minus sign (-)
else:
    text_colour = inkyphat.BLACK
    plus_sign = "+" # Add plus sign (+) to positive number

# Let's throw in some weather icons depending on the price change today
if float(change_percent) < -2:
    icon = base_dir + '/images/icon-storm.png'
elif float(change_percent) < -1 :
    icon = base_dir + '/images/icon-rain.png'
elif float(change_percent) < 0:
    icon = ''
elif float(change_percent) >= 2:
    icon = base_dir + '/images/icon-sun.png'
else:
    icon = ''

change_percent = plus_sign + change_percent + "%"


##########################################################
###  Draw images on the inky display
##########################################################

inkyphat.set_colour(inky_color)
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
time_stamp = latest_trading_day # Stock's Last Trading Day
inkyphat.text((clock_image_x, clock_image_y), time_stamp, inkyphat.BLACK, clock_image_size)

inkyphat.text((5, 5), symbol, inkyphat.BLACK, clock_image_size)

if len(icon) > 0:   # Check that png file is specified before trying to display it
    inkyphat.paste(Image.open(icon), (167, 5))

inkyphat.show()

