#!/usr/bin/python3
#
# https://github.com/bgant/inkyphat-stockmarket/blob/master/inkyphat-stockmarket.py
#
# Brandon Gant
# created: 2018-10-30
# updated: 2019-03-21 Moved from older 'inkyphat' module to newer 'inky' module
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

if inky_type.lower() != "phat":
    print('This script is currently written for the pHAT')
    print('but it should be fairly easy to change to wHAT')
    print('Exiting script...')
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

#import apple_quote
#quote = apple_quote.lookup(symbol)


##########################################################
###  Manipulate the string data for Inky display 
##########################################################

latest_trading_day = quote.day()

price = quote.price()
if len(str(price)) >= 8: 
    price = str(round(float(price)))      # Remove decimals on numbers larger than 9999

change_percent = quote.percent()
change_percent = str(round(float(change_percent[:-1]), 1))    # Strip "%" sign, convert string to float, round to single decimal, convert back to string

# Uncomment hard-coded values for testing
#change_percent = '2.5'
#change_percent = '-1.5'
#change_percent = '-2.5'

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


##########################################################
###  Draw images on the inky display
##########################################################

from inky import InkyPHAT
inky_display = InkyPHAT(inky_color)

# Use BLACK or RED depending on positive or negative change_percent
if '-' in change_percent:
    text_color = inky_display.RED
    plus_sign = "" # number already has minus sign (-)
else:
    text_color = inky_display.BLACK
    plus_sign = "+" # Add plus sign (+) to positive number

inky_display.set_border(text_color)
change_percent = plus_sign + change_percent + "%"


from PIL import Image, ImageFont, ImageDraw
img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

from font_fredoka_one import FredokaOne


def draw_price():
    font = ImageFont.truetype(FredokaOne, 36)
    message = price
    w, h = font.getsize(message)
    x = (inky_display.WIDTH / 2) - (w / 2)
    y = 40 - (h / 2)
    draw.text((x, y), message, text_color, font)


def draw_change_percent():
    font = ImageFont.truetype(FredokaOne, 20)
    message = change_percent
    w, h = font.getsize(message)
    x = (inky_display.WIDTH / 2) - (w / 2)
    y = 70 - (h / 2)
    draw.text((x, y), message, text_color, font)


def draw_date():
    font = ImageFont.truetype(FredokaOne, 11)
    message = latest_trading_day  # Stock's Last Trading Day
    w, h = font.getsize(message)
    x = 150   # Max 212
    y = 90    # Max 104
    draw.text((x, y), message, inky_display.BLACK, font)

def draw_symbol():
    font = ImageFont.truetype(FredokaOne, 11)
    message = symbol
    w, h = font.getsize(message)
    x = 5
    y = 5
    draw.text((x, y), message, inky_display.BLACK, font)

def draw_icon():
    if len(icon) > 0: # Check that png file is specified
        img.paste(Image.open(icon), (167, 5))


# Add each element to the image
draw_price()
draw_change_percent()
draw_date()
draw_symbol()
draw_icon()

# Display the image on the pHAT (or wHAT)
inky_display.set_image(img)
inky_display.show()

