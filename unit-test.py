#!/usr/bin/python3
print('\n')

import AlphaVantage
print('Looking up LMT at www.alphavantage.co...')
print(AlphaVantage.lookup('LMT').data())
print('\n')

import AppleQuote
print('Looking up AAPL at wu-quotes.apple.com...')
print(AppleQuote.lookup('AAPL').data())
print('\n')

import stockmarket
nyse = stockmarket.exchange('nyse')
print("NYSE exchange normally open now? ", nyse.hours()) # Based on business hours only
print("NYSE exchange REALLY open now?   ", nyse.open()) # Connects to Apple Stock service
print('\n')

