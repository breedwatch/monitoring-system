#!/bin/bash

sudo rm -R /home/pi/beemo
git clone https://github.com/breedwatch/monitoring-system /home/pi/beemo
sudo chmod -R 777 /home/pi/beemo
sudo timedatectl set-timezone Etc/UTC

#cd beemo && git pull origin main <-- TODO for later updates!