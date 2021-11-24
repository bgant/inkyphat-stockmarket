## Stock Market Data on a Inky pHat / Raspberry Pi Zero W

![Project Photo](../assets/inkyphat-stockmarket.png)

## Raspberry Pi Zero W

I installed the Flatpak version of the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on my Linux Desktop and used it to write the **Raspberry Pi OS Lite** `2021-10-30-raspios-bullseye-armhf-lite.zip` image to a microSD card.

Mount the `boot` directory on the microSD card and enable SSH:
```console
touch /mnt/boot/ssh
```

Enable Wifi by creating the `wpa_supplicant.conf` file in the boot directory with the following:
```
country=US
update_config=1
ctrl_interface=/var/run/wpa_supplicant
network={
    ssid="YOURSSID"
    psk="YOURPASSWORD"
    scan_ssid=1
}
```

Boot the Raspberry Pi Zero W with the Raspberry Pi OS Lite microSD card:
```console
ssh pi@raspberrypi.local
<default password is "raspberry">
passwd
sudo apt update
sudo apt upgrade
```

## Inky pHat Stock Market Setup

Set Timezone and enable the SPI interface to the Inky pHat:
```console
sudo raspi-config
    5 Localisation Options --> L2 Timezone --> America/<CITY>
    3 Interface Options --> P4 SPI --> Yes
ls /dev/spi*   <-- should see /dev/spidev0.0 and /dev/spidev0.1
```

Use a Python Virtual Environment and upgrade `pip` packages:
```console
sudo apt install python3-venv
python3 -m venv --system-site-packages ~/inkyphat-env
source ~/inkyphat-env/bin/activate
```

Download and use this Git Repository:
```console
sudo apt install git
git clone https://github.com/bgant/inkyphat-stockmarket
cd ~/inkyphat-stockmarket
```

Install Python packages in virtual environment using `pip`:
```console
python3 -m pip install -r requirements.txt
sudo apt install libatlas-base-dev libopenjp2-7
```

Initialize and Configure Scripts:
```console
python3 inkyphat-stockmarket.py    <-- First run creates your own inkyphat-stockmarket.ini file
vi inkyphat-stockmarket.ini
    api = <YOUR API KEY>           <-- Sign up for Free API key at https://finnhub.io
    exchange_hours = disabled      <-- For testing when market is closed
python3 inkyphat-stockmarket.py    <-- Display should show the last Dow Jones Index price
deactivate                         <-- Exit Python virtual environment
````

Update the Inky pHat display every 5 Minutes when the Stock Market is open:
```console
vi inkyphat-stockmarket.ini
    exchange_hours = enabled
sudo vi /etc/crontab
    */5 * * * 1-5 pi nice /home/pi/inkyphat-env/bin/python3 /home/pi/inkyphat-stockmarket/inkyphat-stockmarket.py > /dev/null 2>&1 &
sudo reboot
```

## More Information:
* [Getting Started with Inky pHAT](https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat)
* [Getting Started with the Raspberry Pi Zero Wireless](https://learn.sparkfun.com/tutorials/getting-started-with-the-raspberry-pi-zero-wireless)
* [Inky pHAT Pinout](https://pinout.xyz/pinout/inky_phat)
