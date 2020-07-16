# https://github.com/bgant/inkyphat-stockmarket/commits/master/packages/stockmarket.py
#
# Brandon Gant
# Created: 2018-12-07
#
#
# command line:
#
#    python3 stockmarket.py nyse
#
#
# Python3 script:
# 
#    import stockmarket
#    nyse = stockmarket.exchange('NYSE')
#    nyse.hours()
#    nyse.status()
#

class exchange:
    def __init__(self, exchange):
        self.exchange = exchange.upper()

        # Import data from YAML file with stock exchange information
        import yaml
        with open('stockmarket.yaml', 'rt') as yaml_file:
            yaml_text = yaml_file.read()
        yaml_data = yaml.safe_load(yaml_text)
        self.yaml = yaml_data[self.exchange]


    def hours(self):
        ##########################################################
        ###  Is this Stock Exchange typically open now? 
        ##########################################################
        #
        # List of Stock Exchange Trading Hours:
        #   https://en.wikipedia.org/wiki/List_of_stock_exchange_trading_hours
        #
        # The United States New York Stock Exchange and NASDAQ are in the Eastern Time Zone.
        # They are open from 9:30 to 16:00 and follow Daylight Savings Time (+1 to hours).
        #
        # Eastern Standard Time (EST) is UTC -05:00 (markets open 14:30 to 21:00 UTC)
        # Eastern Daylight Time (EDT) is UTC -04:00 (markets open 15:30 to 22:00 UTC)
        #

        # Instead of creating a multi-line "function", we can do the same thing with a single-line "lamba"
        import pytz
        from datetime import datetime
        isDST_now_in = lambda zonename: bool(datetime.now(pytz.timezone(zonename)).dst())

        # Are we currently in Daylight Savings or not? If so add one hour.
        if isDST_now_in(self.yaml['location']) == True:
           self.yaml['market_open'] -= 100
           self.yaml['market_close'] -= 100

        # Markets are closed Saturday and Sunday
        day_of_the_week = int(datetime.utcnow().strftime("%u"))   # The day of the week range 1 to 7 with Monday being 1

        # Current hour and minute as an integer
        time_now = int(str(datetime.utcnow().hour) + str(datetime.utcnow().minute))

        # If market opens before Midnight UTC and closes after Midnight UTC
        if self.yaml['market_open'] > self.yaml['market_close']:
            if time_now >= self.yaml['market_open'] or time_now <= self.yaml['market_close']:
                return True # Exchange should be open
            else:
                return False # Exchange should be closed
        # If market opens after Midnight UTC and closes before Midnight UTC
        elif self.yaml['market_open'] <= time_now <= self.yaml['market_close'] and day_of_the_week <= 5:
            return True # Exchange should be open
        else:
            return False # Exchange should be closed


    def status(self):
        ##########################################################
        ###  Is this Stock Exchange REALLY open now?      
        ##########################################################
        #
        # Use Apple Stock service to check if a Stock Exchange is actually open or not
        #    Source: https://stackoverflow.com/questions/9428989/how-to-test-if-the-stock-market-nyse-is-currently-open-closed
        #

        symbol = self.yaml['symbol']

        import apple_quote
        return apple_quote.lookup(symbol).status()


# This section allows you to run the module directly for testing
#   i.e. python3 stockmarket.py NYSE
#
#   Source: https://docs.python.org/2/tutorial/modules.html
#
if __name__ == "__main__":
    import sys
    print("Is the", sys.argv[1].upper(), "exchange Normally open now?     ", exchange(sys.argv[1]).hours())
    #print("Is the", sys.argv[1].upper(), "exchange REALLY open right now? ", exchange(sys.argv[1]).status())
