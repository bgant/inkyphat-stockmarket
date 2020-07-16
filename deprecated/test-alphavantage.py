#!/usr/bin/python3
#
# Usage:
#   python3 unit-test.py

symbol="DIA"
#symbol="MSFT"

import alphavantage
print('Looking up %s at www.alphavantage.co...' % symbol)
test1 = alphavantage.lookup(symbol)
print('price:'.rjust(9),   test1.price().rjust(11))
print('percent:'.rjust(9), test1.percent().rjust(11))
print('day:'.rjust(9),     test1.day().rjust(11))
print('data:'.rjust(9),    test1.data())
