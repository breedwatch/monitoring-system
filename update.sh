#!/bin/bash

rm -R /home/pi/beemo
git clone https://github.com/breedwatch/monitoring-system /home/pi/beemo
chmod -R 777 /home/pi/beemo
sudo timedatectl set-timezone Etc/UTC
sudo rm conf.ini
wget https://raw.githubusercontent.com/breedwatch/monitoring-system/main/conf.ini /home/pi/beemo/conf.ini
sudo chmod 777 /home/pi/conf.ini

if grep -Fxq "# 0.1.6rev4" /home/pi/beemo/main.py
then
   echo "ok!";
else
  echo "nope!"
fi