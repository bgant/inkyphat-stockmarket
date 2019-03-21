#!/usr/bin/python3
#
# https://github.com/bgant/inkyphat-stockmarket/blob/master/inkyphat-stockmarket.py
#
# Brandon Gant
# created: 2018-10-30
#

import os
# Move into the base directory of this script to import other files
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
    shutil.copyfile(base_dir + '/template/inkyphat-stockmarket.ini.sample', base_dir + '/inkyphat-stockmarket.ini')
    exit()
symbol         = config.get('inkyphat_stockmarket', 'symbol')
exchange_name  = config.get('inkyphat_stockmarket', 'exchange_name')
inky_type      = config.get('inkyphat_stockmarket', 'inky_type')
inky_color     = config.get('inkyphat_stockmarket', 'inky_color')
exchange_hours = config.get('inkyphat_stockmarket', 'exchange_hours')
apikey         = config.get('inkyphat_stockmarket', 'apikey')

if apikey == '':
    print('Go to http://alphavantage.co to sign up for a free API key')
    exit()


##########################################################
###  Update the display only if the Exchange is open?
##########################################################
if exchange_hours == 'enabled':
    import stockmarket
    exchange_open = stockmarket.exchange(exchange_name).hours() 
    if exchange_open == False:
        print('exchange_hours enabled:', exchange_name.upper(), 'exchange is currently closed... Exiting')
        exit()
    else:
        print('exchange_hours enabled:', exchange_name.upper(), 'exchange is currently open... Updating Inky display')
else:
    print('exchange_hours disabled: Updating Inky display')


##########################################################
###  Download the stock data (multiple options)
##########################################################

import alphavantage
quote = alphavantage.lookup(symbol)

#import apple_finance
#quote = apple_finance.lookup(symbol)


##########################################################
###  Manipulate the string data for Inky display 
##########################################################

latest_trading_day = quote.day()

price = quote.price()
if len(str(price)) >= 8: 
    price = str(round(float(price)))      # Remove decimals on numbers larger than 9999

change_percent = quote.percent()
change_percent = str(round(float(change_percent[:-1]), 1))    # Strip "%" sign, convert string to float, round to single decimal, convert back to string

if '-' in change_percent:
    text_color = 'inky_display.RED'
    plus_sign = "" # number already has minus sign (-)
else:
    text_color = 'inky_display.BLACK'
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

from inky import InkyPHAT

if inky_type.lower() != "phat":
    print('This script is currently written for the pHAT')
    print('but it should be fairly easy to change to wHAT')
    print('Exiting script...')
    import sys
    sys.exit()

inky_display = InkyPHAT(inky_color)
inky_display.set_border(text_color)

from PIL import Image, ImageFont, ImageDraw
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

from font_fredoka_one import FredokaOne


print(inky_type, inky_color, text_color)

def price_image():
    font = ImageFont.truetype(FredokaOne, 36)
    message = str(price)
    w, h = font.getsize(message)
    x = (inky_display.WIDTH / 2) - (w / 2)
    y = 40 - (h / 2)
    #draw.text((x, y), message, text_color, font)
    draw.text((x, y), message, inky_display.RED, font)

price_image()



#price_image_size = ImageFont.truetype(inkyphat.fonts.FredokaOne, price_font_size)
#price_image_width, price_image_height = inkyphat.textsize(price, price_image_size)
#price_image_x = (inkyphat.WIDTH / 2) - (price_image_width / 2)
#price_image_y = 40 - (price_image_height / 2)
#inkyphat.text((price_image_x, price_image_y), price, text_colour, price_image_size)

#change_percent_font_size = 20
#change_percent_image_size = ImageFont.truetype(inkyphat.fonts.FredokaOne, change_percent_font_size)
#change_percent_image_width, change_percent_image_height = inkyphat.textsize(change_percent, change_percent_image_size)
#change_percent_image_x = (inkyphat.WIDTH / 2) - (change_percent_image_width / 2)
#change_percent_image_y = 70 - (change_percent_image_height / 2)
#inkyphat.text((change_percent_image_x, change_percent_image_y), change_percent, text_colour, change_percent_image_size)

#clock_font_size = 11
#clock_image_size = ImageFont.truetype(inkyphat.fonts.FredokaOne, clock_font_size)
#clock_image_x = 150   # Max 212
#clock_image_y = 90    # Max 104
#time_stamp = latest_trading_day # Stock's Last Trading Day
#inkyphat.text((clock_image_x, clock_image_y), time_stamp, inkyphat.BLACK, clock_image_size)

#inkyphat.text((5, 5), symbol, inkyphat.BLACK, clock_image_size)

#if len(icon) > 0:   # Check that png file is specified before trying to display it
#    inkyphat.paste(Image.open(icon), (167, 5))

inky_display.set_image(img)
inky_display.show()

