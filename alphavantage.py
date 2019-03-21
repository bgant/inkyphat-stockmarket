# https://github.com/bgant/inkyphat-stockmarket/blob/master/packages/alphavantage.py
#
# Brandon Gant
# Created: 2018-12-07
#
#
# command line:
#
#   python3 alphavantage.py MSFT
#
#
# Python3 script:
#
#   import alphavantage
#   msft = alphavantage.lookup('MSFT')
#   msft.data()
#   msft.price()
#

class lookup:
    def __init__(self, symbol):
        self.symbol = symbol.lower()

        import configparser
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('inkyphat-stockmarket.ini')
        apikey  = config.get('inkyphat_stockmarket', 'apikey')

        if apikey == '':
            print('Go to http://alphavantage.co to sign up for a free API key')
            exit()

        import requests
        url="https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={apikey}".format(symbol=self.symbol, apikey=apikey)
        response = requests.get(url)
        #print(response.text)          # Uncomment to see raw JSON response from server
        self.response = response.json()         # Convert response string data to json data

    def data(self):
        self.data = self.response
        return self.data

    def price(self):
        self.price = self.response['Global Quote']['05. price']
        self.price = round(float(self.price),2)         # Round to two decimals 
        self.price = str("{:.2f}".format(self.price))   # Print trailing zeros after decimal if needed
        return self.price

    def percent(self):
        self.percent = self.response['Global Quote']['10. change percent']
        self.percent = str(float(self.percent[:-1])) # Strip "%" sign, convert string to float, convert back to string
        return self.percent

    def day(self):
        self.day = self.response['Global Quote']['07. latest trading day']
        return self.day

# This section allows you to run the module directly for testing
#   Source: https://docs.python.org/2/tutorial/modules.html
if __name__ == "__main__":
    import sys
    test = lookup(sys.argv[1])
    print('price:'.rjust(9), test.price().rjust(11))
    print('percent:'.rjust(9), test.percent().rjust(11))
    print('day:'.rjust(9), test.day().rjust(11))
    print('data:'.rjust(9), test.data())
