#!/bin/bash

ping -c1 -W1 -q 8.8.8.8 &>/dev/null
status=$( echo $? )
if [[ $status == 0 ]] ; then
     rm -R /home/pi/beemo
     git clone https://github.com/breedwatch/monitoring-system /home/pi/beemo
     sudo timedatectl set-timezone Etc/UTC
else
     echo "no internet connection - abort!"
fi