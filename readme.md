READ BEFORE BOOT


# First Boot
- LED blinks blue 3 times: scale is not calibrated
- LED turns on red: remove all items from scalce (30 Seconds)
- LED turns on green: put the weight (calibrate_weight in the conf.ini) on the scale (30 Seconds)
- LED blinks green 3 times: all done. Reboot system


# put USB Stick into the Device
- LED blinks green 3 times: stick is mounted, works okay
- LED turns on green: all done! remove the stick from the device (30 Seconds)


# conf.ini

[DEFAULT] <br>
**please use international standard (database names):  https://en.wikipedia.org/wiki/List_of_tz_database_time_zones** <br>
`timezone = Europe/Berlin` <br>

**device_name is also the device id! No spaces or special charakters allowed!** <br>
`device_name = dev_device`   <br>

**device location for further purpose? just like Names or GPS Data** <br>
`device_location = Basement` <br>

**seconds of every cycle to gather data** <br>
`app_wait_seconds = 900` <br>

**not implemented yet** <br>
`errors_before_restart = 3` <br>

**median for all dataset data (excluding aht and fft)** <br>
`median = 5` <br>

**option to delete all data from SD after transfer the data to USB device** <br>
`delete_after_usb = 0` <br>

[AUDIO] <br>
**how long the microphone record** <br>
`duration = 180` <br>

**sample rate** <br>
`fs = 8000` <br>

**True (or 1): the microphone samples .wav files (0.061mb per Second)** <br>
`wav=0` <br>

**true: the microphone samples fft data** <br>
`fft=1` <br>

[SCALE] <br>
`ratio = 29.805333333333333` <br>
`offset = 8512671.5` <br>
`calibrated = 1` <br>

**weight in grams to calibrate with** <br>
`calibrate_weight = 7500` <br>

**turn on sensors** <br>
[SENSORS] <br>
`scale=0` <br>
`dht22=0` <br>
`ds18b20=0` <br>
`microphone=0` <br>
`aht20=0` <br>

