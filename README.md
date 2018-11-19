## Display Stock Market Data on inky pHat / Raspberry Pi Zero W

![Project Photo](../assets/inkyphat-stockmarket.png)

### How to Use:
* inkyphat-stockmarket.py is the main script that downloads the latest stock price and displays it on the screen. You can manually run this script as often as you like.
* inkyphat-stockmarket-launcher.py is run by /etc/crontab. It checks to see if the Stock Market is open before running the inkyphat-stockmarket.py script.

### To Do List:
* Replace 'inkyphat.RED' statements with variable to handle inkyphat.YELLOW or inkyphat.BLACK
* Add requirements.txt file for imports
* Use UTC instead of CST
* Use ConfigParser with settings.txt file (https://docs.python.org/3/library/configparser.html)
* Add instructions and images for building and setting up inky pHat on Raspberry Pi Zero W

### More Information:
* [Getting Started with Inky pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)
* [Getting Started with the Raspberry Pi Zero Wireless](https://learn.sparkfun.com/tutorials/getting-started-with-the-raspberry-pi-zero-wireless)
