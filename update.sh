#!/bin/bash

git init beemo
cd /home/pi/beemo && git remote add origin https://github.com/breedwatch/monitoring-system.git
cd /home/pi/beemo && git pull origin main
sudo chmod -R 777 /home/pi/beemo
sudo timedatectl set-timezone Etc/UTC

#cd beemo && git pull origin main <-- TODO for later updates!