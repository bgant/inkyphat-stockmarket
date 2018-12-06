#!/usr/bin/python3

import stockmarket

nyse = stockmarket.exchange('nyse')

print("Exchange normally open now? ", nyse.hours()) # Based on business hours only

print("Exchange REALLY open now? ", nyse.open()) # Connects to Apple Stock service

