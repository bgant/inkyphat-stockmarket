#!/usr/bin/python3
#
# Usage:
#   python3 unit-test.py

print('\n')

print('Testing alphavantage.py module...')
import alphavantage
print('Looking up ^DJI at www.alphavantage.co...')
test1 = alphavantage.lookup('^DJI')
print('price:'.rjust(9),   test1.price().rjust(11))
print('percent:'.rjust(9), test1.percent().rjust(11))
print('day:'.rjust(9),     test1.day().rjust(11))
print('data:'.rjust(9),    test1.data())
print('\n')

