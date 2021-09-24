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



# todo alle Inhalte von /media/usb* in /media/usb verschieben
# todo conf.ini verbleibt auf dem USB Stick und wird nicht geloescht. Sollte aber geloescht werden nach dem aendern!


for VARIABLE in 1 2 3 4 5 .. N
do
	command1
	command2
	commandN
done