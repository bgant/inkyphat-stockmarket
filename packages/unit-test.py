#!/usr/bin/python3

# Move into the directory of this script
import os.path
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print('\n')

import alphavantage
print('Looking up ^DJI at www.alphavantage.co...')
test1 = alphavantage.lookup('^DJI')
print('price:'.rjust(9),   test1.price().rjust(11))
print('percent:'.rjust(9), test1.percent().rjust(11))
print('day:'.rjust(9),     test1.day().rjust(11))
print('data:'.rjust(9),    test1.data())
print('\n')

import apple_finance
print('Looking up ^DJI at wu-quotes.apple.com...')
test2 = apple_finance.lookup('^DJI')
print('price:'.rjust(9),   test2.price().rjust(11))
print('percent:'.rjust(9), test2.percent().rjust(11))
print('day:'.rjust(9),     test2.day().rjust(11))
print('status:'.rjust(9),  str(test2.status()).rjust(11))
print('data:'.rjust(9),    test2.data())
print('\n')

import stockmarket
nyse = stockmarket.exchange('nyse')
print("NYSE exchange normally open now? ", nyse.hours()) # Based on business hours only
print("NYSE exchange REALLY open now?   ", nyse.status()) # Connects to Apple Stock service
print('\n')

