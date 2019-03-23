## Display Stock Market Data on inky pHat / Raspberry Pi Zero W

![Project Photo](../assets/inkyphat-stockmarket.png)

### How to Use:
* `sudo raspi-config`
  * `5 Interfacing Options --> P4 SPI --> Yes` (enable SPI interface)
  * `ls /dev/spi*` (should see /dev/spidev0.0  /dev/spidiv0.1)
* `sudo apt-get install git python3-pip libopenjp2-7 libtiff5`
* `git clone https://github.com/bgant/inkyphat-stockmarket`
* `pip3 install -r requirements.txt` (walk away... this is going to take a long time)
* `python3 inkyphat-stockmarket.py` (initializes your own config file)
* Go to https://alphavantage.co and sign up for your free API key
  * Add your API key to **inkyphat-stockmarket.ini**
* Add line to **/etc/crontab** to update the display every five minutes (when the market is open) 
  * `*/5 * * * 1-5 pi nice /home/pi/inkyphat-stockmarket/inkyphat-stockmarket.py > /dev/null 2>&1 &`

### More Information:
* [Getting Started with Inky pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)
* [Getting Started with the Raspberry Pi Zero Wireless](https://learn.sparkfun.com/tutorials/getting-started-with-the-raspberry-pi-zero-wireless)
* [Inky pHAT Pinout](https://pinout.xyz/pinout/inky_phat)
