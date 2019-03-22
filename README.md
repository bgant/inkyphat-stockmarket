## Display Stock Market Data on inky pHat / Raspberry Pi Zero W

![Project Photo](../assets/inkyphat-stockmarket.png)

### How to Use:
* `sudo apt-get install git python3-pip`
* `git clone https://github.com/bgant/inkyphat-stockmarket`
* `pip3 install -r requirements.txt`
* `python3 inkyphat-stockmarket.py` (initializes your own config file)
* Go to https://alphavantage.co and sign up for your free API key
  * Add your API key to **inkyphat-stockmarket.ini**
* Add an entry to **/etc/crontab** to update the display automatically

### More Information:
* [Getting Started with Inky pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)
* [Getting Started with the Raspberry Pi Zero Wireless](https://learn.sparkfun.com/tutorials/getting-started-with-the-raspberry-pi-zero-wireless)
