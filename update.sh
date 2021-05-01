#!/bin/bash

rm -R beemo
git clone https://github.com/breedwatch/monitoring-system beemo
chmod -R 777 /home/pi/beemo
sudo timedatectl set-timezone Etc/UTC
sudo rm conf.ini
wget https://raw.githubusercontent.com/breedwatch/monitoring-system/main/conf.ini
sudo chmod 777 conf.ini

#cd beemo && git pull origin main <-- TODO for later updates!