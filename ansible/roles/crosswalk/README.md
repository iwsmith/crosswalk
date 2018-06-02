crossXwalk Sign
===============

This role configures a RaspberryPi to run the software powering one of the
crossXwalk signs.


## RaspberryPi Setup

Make sure you've done the soldering and connection work to attach the hat to the
pi, then set up the AdaFruit drivers by following these instructions:

https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices

The result should be a `/home/pi/???` directory. Build the image-viewer utility:

```shell
$ sudo apt-get install ???
$ cd ???/util
$ make led-image-viewer
```
