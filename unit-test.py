#!/usr/bin/python3
print('\n')

import alphavantage
print('Looking up LMT at www.alphavantage.co...')
lmt = alphavantage.lookup('LMT')
print('data:', lmt.data())
print('price:', lmt.price())
print('\n')

import apple_finance
print('Looking up AAPL at wu-quotes.apple.com...')
aapl = apple_finance.lookup('AAPL')
print('data:', aapl.data())
print('price:', aapl.price())
print('status:', aapl.status())
print('\n')

import stockmarket
nyse = stockmarket.exchange('nyse')
print("NYSE exchange normally open now? ", nyse.hours()) # Based on business hours only
print("NYSE exchange REALLY open now?   ", nyse.open()) # Connects to Apple Stock service
print('\n')

