#!/bin/bash

sudo rm -R /home/pi/beemo
git clone https://github.com/breedwatch/monitoring-system beemo
sudo chmod -R 777 /home/pi/beemo