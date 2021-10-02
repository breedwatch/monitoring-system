#!/bin/bash

if grep -Fxq "# 0.1.7" /home/pi/beemo/main.py
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

