#!/usr/bin/python3
print('\n')

import alphavantage
print('Looking up ^DJI at www.alphavantage.co...')
test1 = alphavantage.lookup('^DJI')
print('data:',    test1.data())
print('price:',   test1.price())
print('percent:', test1.percent())
print('day:',     test1.day())
print('\n')

import apple_finance
print('Looking up ^DJI at wu-quotes.apple.com...')
test2 = apple_finance.lookup('^DJI')
print('data:',    test2.data())
print('price:',   test2.price())
print('percent:', test2.percent())
print('day:',     test2.day())
print('status:',  test2.status())
print('\n')

import stockmarket
nyse = stockmarket.exchange('nyse')
print("NYSE exchange normally open now? ", nyse.hours()) # Based on business hours only
print("NYSE exchange REALLY open now?   ", nyse.open()) # Connects to Apple Stock service
print('\n')

