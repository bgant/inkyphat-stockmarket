#!/usr/bin/python3
#
# Usage:
#   python3 unit-test.py

symbol='AAPL'

import apple_quote
print('Looking up %s at wu-quotes.apple.com...' % symbol)
test2 = apple_quote.lookup(symbol)
print('price:'.rjust(9),   test2.price().rjust(11))
print('percent:'.rjust(9), test2.percent().rjust(11))
print('day:'.rjust(9),     test2.day().rjust(11))
print('status:'.rjust(9),  str(test2.status()).rjust(11))
print('data:'.rjust(9),    test2.data())
