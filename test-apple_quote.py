#!/usr/bin/python3
#
# Usage:
#   python3 unit-test.py

print('\n')

print('Testing apple_quote.py module...')
import apple_quote
print('Looking up ^DJI at wu-quotes.apple.com...')
test2 = apple_quote.lookup('^DJI')
print('price:'.rjust(9),   test2.price().rjust(11))
print('percent:'.rjust(9), test2.percent().rjust(11))
print('day:'.rjust(9),     test2.day().rjust(11))
print('status:'.rjust(9),  str(test2.status()).rjust(11))
print('data:'.rjust(9),    test2.data())
print('\n')

