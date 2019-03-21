#!/usr/bin/python3
#
# Usage:
#   python3 unit-test.py

print('\n')

print('Testing stockmarket.py module...')
import stockmarket
nyse = stockmarket.exchange('nyse')
print("NYSE exchange normally open now? ", nyse.hours()) # Based on business hours only
print("NYSE exchange REALLY open now?   ", nyse.status()) # Connects to Apple Stock service
print('\n')

