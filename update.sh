#!/bin/bash

rm -R /home/pi/beemo
git clone https://github.com/breedwatch/monitoring-system /home/pi/beemo
sudo timedatectl set-timezone Etc/UTC
sudo rm conf.ini
wget https://raw.githubusercontent.com/breedwatch/monitoring-system/main/conf.ini /home/pi/beemo/conf.ini

if grep -Fxq "# 0.1.6rev6" /home/pi/beemo/main.py
then
   echo "beemo ok!";
else
  echo "beemo NOT OK!"
fi

if grep -Fxq "timezone = Etc/UTC" /home/pi/conf.ini
then
   echo "config ok!";
else
  echo "config NOT OK!"
fi