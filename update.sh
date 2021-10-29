#!/bin/bash

wget -q --spider http://google.com

if [ $? -eq 0 ]; then
     # uncomment for tmp117 support
     # sudo pip3 install adafruit-circuitpython-tmp117

     # install for new version > 1.8
     sudo pip3 install GitPython

     rm -R /home/pi/beemo
     git clone https://github.com/breedwatch/monitoring-system /home/pi/beemo
     sudo timedatectl set-timezone Etc/UTC
else
     echo "no internet connection - abort!"
fi