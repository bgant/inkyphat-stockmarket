#
# Source: https://stackoverflow.com/questions/9428989/how-to-test-if-the-stock-market-nyse-is-currently-open-closed
#
# command line:
#
#   python3 AlphaVantage.py MSFT
#
#
# Python3 script:
#
#   import AlphaVantage
#   msft = AlphaVantage('MSFT').lookup()
#   msft.data()
#   msft.data['05. price']
#

class lookup:
    def __init__(self, symbol):
        self.symbol = symbol.lower()

    def data(self):

        # This is where you put your https://www.alphavantage.co API key
        dir = "/home/pi/inkyphat-stockmarket/"
        apifile = dir + "apikey.txt"
        # Keep the apikey separate and away from the Github repo using .gitignore

        import os.path
        if os.path.isfile(apifile) and os.path.getsize(apifile) > 1:
            apikey = str(open(apifile).read()).strip("\n")
        else:
            print(apifile, "file is missing or is empty")
            print("Get a free API key from https://www.alphavantage.co")
            exit()

        import requests
        url="https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={apikey}".format(symbol=self.symbol, apikey=apikey)
        response = requests.get(url)
        #print(response.text)          # Uncomment to see raw JSON response from server
        data = response.json()         # Convert response string data to json data
        return data['Global Quote']

# This section allows you to run the module directly for testing
#   Source: https://docs.python.org/2/tutorial/modules.html
if __name__ == "__main__":
    import sys
    print(lookup(sys.argv[1]).data())
