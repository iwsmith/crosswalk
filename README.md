crossXwalk Sign
===============

This repository holds the code and configuration for running a RaspberryPi to
power one of the crossXwalk signs.


## RaspberryPi Setup

Make sure you've done the soldering and connection work to attach the hat to the
pi, then set up the AdaFruit drivers for the
[RGB Matrix plus Real Time Clock Hat](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices).

Log into the pi and set things up:

```shell
# Upgrade and prepare for Ansible management
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install python

# Download and install drivers
$ wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh
$ sudo bash rgb-matrix.sh
# Answer (2) for Adafruit RGB Matrix HAT + RTC
# Answer (Y) to enable realtime clock support
# Answer (2) for the 'convenience' optimization level

# Build the image viewer tool
$ cd rpi-rgb-led-matrix/util
$ make led-image-viewer
```


## Deployment

Run ansible from your development machine to configure the host and deploy the
code:

```shell
$ ansible-playbook site.yml -i inventory.ini [-l crosswalk-x] [-C] [-D]
```


## Content

### Creating New Voice Commands
On a Mac `say -v Samantha "Walk Sign Is On. Walk Now." --data-format=LEF32@22050 -o walk_now.wav` 
