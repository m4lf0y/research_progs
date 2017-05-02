#! /bin/sh
#GPS data transformation

sudo gpsctl -f -n /dev/tty.usbserial
sudo stty -F /dev/tty.usbserial ispeed 4800
gpsd -b /dev/tty.usbserial
sudo cat /dev/tty.usbserial
