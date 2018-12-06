#
# Source: https://stackoverflow.com/questions/9428989/how-to-test-if-the-stock-market-nyse-is-currently-open-closed
#
# command line:
#
#   python3 apple_finance.py AAPL
#
#
# Python3 script:
#
#   import apple_finance
#   aapl = apple_finance.lookup('AAPL')
#   appl.data()
#   appl.price()
#

class lookup:
    def __init__(self, symbol):
        self.symbol = symbol.lower()

        imei = '42' # Apparently any random UID will work??
      
        url='http://wu-quotes.apple.com/dgw?imei=' + imei + '&apptype=finance'
        headers = {'Content-Type': 'application/xml'}

        # Create XML data to POST to Apple API
        xml = "<?xml version='1.0' encoding='utf−8'?><request devtype='Apple_OSX' deployver='APPLE_DASHBOARD_1_0' \
               app='YGoAppleStocksWidget' appver='unknown' api='finance' apiver='1.0.1' acknotification='0000'><query id='0' \
               timestamp='`date +%s000`' type='getquotes'><list><symbol>"
        xml = xml + self.symbol
        xml = xml + "</symbol></list></query></request>"
        xml = xml.encode('utf-8')

        # Send XML data to API to get response
        import requests
        response = requests.post(url=url, data=xml, headers=headers)
        #print(response.text) # See the raw XML response from the server

        # Parse XML response into dictionary list of key-value pairs
        from xml.etree import ElementTree
        root = ElementTree.fromstring(response.content)
        #print(root[0][0][0][6].text) # Crude way to manually select values from the XML response

        self.results = {} # Initialize dictionary variable to hold XML response key-value pairs
        for child in root.iter(): # Interate through each element in the XML response
            #print(child.tag, child.attrib, child.text) # View the values for each element
            self.results.update({child.tag:child.text}) # Add key-value pairs to the dictionary

    def data(self):
        return self.results

    def price(self):
        self.price = self.results['price']
        return self.price

    def percent(self):
        self.percent = self.results['changepercent']
        return self.percent

    def day(self):
        import time
        self.day = self.results['timestamp'] # Epoch Time value
        self.day = int(self.day) # string converted to integer for localtime function
        self.day = time.strftime('%Y-%m-%d', time.localtime(self.day)) # Year-Month-Day value 
        return self.day

    def status(self):
        self.status = self.results['status']
        if self.status == '0':
            return False
        else:
            return True

# This section allows you to run the module directly for testing
#   Source: https://docs.python.org/2/tutorial/modules.html
if __name__ == "__main__":
    import sys
    test = lookup(sys.argv[1])
    print('data:', test.data())
    print('price:', test.price())
    print('percent:', test.percent()) 
    print('day:', test.day())
    print('status:', test.status())
