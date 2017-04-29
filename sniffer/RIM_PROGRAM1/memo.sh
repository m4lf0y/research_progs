#! /bin/sh
#GPS data transformation

sudo gpsctl -f -n /dev/ttyUSB0
sudo stty -F /dev/ttyUSB0 ispeed 4800
gpsd -b /dev/ttyUSB0
sudo cat /dev/ttyUSB0
