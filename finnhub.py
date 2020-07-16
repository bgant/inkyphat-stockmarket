# https://github.com/bgant/inkyphat-stockmarket/blob/master/packages/finnhub.py
# https://finnhub.io/docs/api
#
# Brandon Gant
# Created: 2020-07-16
#
#
# command line:
#
#   python3 finnhub.py MSFT
#
#
# Python3 script:
#
#   import finnhub
#   msft = finnhub.lookup('MSFT')
#   msft.data()
#   msft.price()
#

class lookup:
    def __init__(self, symbol):
        self.symbol = symbol.upper()

        import configparser
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('inkyphat-stockmarket.ini')
        apikey  = config.get('inkyphat_stockmarket', 'apikey')

        if apikey == '':
            print('Go to http://finnhub.io to sign up for a free API key')
            import sys
            sys.exit()

        import requests
        url="https://finnhub.io/api/v1/quote?token={apikey}&symbol={symbol}".format(symbol=self.symbol, apikey=apikey)
        #print(url)
        response = requests.get(url)
        #print(response.text)              # Uncomment to see raw JSON response from server
        self.response = response.json()    # Convert response string data to json data

    def data(self):
        self.data = self.response
        return self.data

    def price(self):
        self.price = self.response['c']
        self.price = round(float(self.price),2)         # Round to two decimals 
        self.price = str("{:.2f}".format(self.price))   # Print trailing zeros after decimal if needed
        return self.price

    def percent(self):
        self.current = self.response['c']
        self.previousclose = self.response['pc']
        self.percent = str(round((self.current - self.previousclose) / self.previousclose * 100, 1))  # Calculate Percentage, Round to one decimal, Convert to String
        return self.percent

    def day(self):
        from time import localtime
        self.unixtime = localtime(self.response['t'])
        self.day = "%s-%s-%s" % (self.unixtime.tm_year, str(self.unixtime.tm_mon).zfill(2), str(self.unixtime.tm_mday).zfill(2))
        return self.day

# This section allows you to run the module directly for testing
#   Source: https://docs.python.org/2/tutorial/modules.html
if __name__ == "__main__":
    import sys
    test = lookup(sys.argv[1])
    print('raw data:'.rjust(9), test.data())
    print('price:'.rjust(9), test.price().rjust(11))
    print('percent:'.rjust(9), test.percent().rjust(11))
    print('day:'.rjust(9), test.day().rjust(11))
