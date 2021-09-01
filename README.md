crossXwalk Sign
===============

This repository holds the code and configuration for running a RaspberryPi to
power one of the crossXwalk signs.


## Concepts

The crossXwalk can run in a number of different _modes_. The modes determine
the sign display, audio, and interactivity.

- **off** - no display or sound
- **demo** - run one of the demo programs shipped with the LED drivers
- **image** - display a single image on loop
- **walk** - main crosswalk interaction mode

When in crossing mode, the signs will react to button presses by generating a
_scene_, composed of an _intro_, _walk_, and _outro_ animations. The signs then
synchronize and start playing the scene together. Once the scene is over, the
sign returns to a standby 'halt' image.


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

### Creating gifs in Photoshop
Using photoshop's timeline, create a frame animation. Timing for each walk is set using the frame delay. Even single images need at least two visually distinct frames (for whatever reason, the the software doesn't respect the frame delay if there are two identitcal frames). Most walks have two frames, one with a dark grey pixel in a corner, and a delay that matches with the length of the audio. Loop count should be set to "Once" in the timeline.

In the config file, the loops attribute should have a value of 1.

## Moving to HQ Mode
1. Move the button from pin 18 to pin 19 on the HAT
1. Solder a jumper wire between pin 4 and 18. See [this diagram](https://github.com/hzeller/rpi-rgb-led-matrix/blob/master/img/adafruit-mod.jpg)
1. Reinstall the drivers (see above), this time selecting option one in the last step (quality). Make sure you `wget` the latest script, don't just re-run what's on device.

## Improving Quality
`echo "isolcpus=3" >> /boot/cmdline.txt`

## Scheduling
In `config.yml` we define walks and schedules for when they run:
```
walks:
  chimchim:
    category: ad
    loops: 1
  gif-dots:
    category: inactive
    loops: 10
    audio: trip.wav
```

The above defines a walk called `chimchim`, that is in the `ad` category and loops only once.
It also defines a walk called `gif-dots` that is in the `inactive` category, loops 10 times, and plays the audiofile `trip.wav`. By default walks will attempt to play a sound file matching their name (e.g. `chimchim.wav`). Similarly the gif that is played will be `chimchim.gif`.

### Weights
Weights are used to set how often walks from a given category are played. By default all walks have a weight of one. You can specify a custom weighting scheme as seen below for `demo`. Any category not explicitly listed in a weighting scheme will use the default.
```
weights:
  all:
    _: 1
  demo:
    actions: 18
    actionscharade: 7
    actionsplus: 20
    ad: 0
    airguitar: 2
    animals: 11
    animalsplus: 8
    dance: 10
    fin: 0
    game: 1
    karaoke: 2
    language: 7
    normal: 7
    normalish: 7
    rare: 2
    rps: 2
    silly: 11
    sleep: 0
    social: 10
    trip: 0
```

### Menu
The menu section allows you to define an active weighting scheme by time. The scheme that is the most recently set will be active (that is, the start time is in the most recently passed). In the below example the demo weighting scheme will be activate after 1:45 AM on August 1st, 2021. 
```
menu:
  - start: '2021-08-01T01:45:00'
    weights: demo
```

### Schedule
You can also schedule a walk to play at a specific time. In the below example the `workoutWednesday` walk will play at 2100 on July 6th, 2019. Ads are automatically generated and run in the hour preceeding the event to let people know whats happening and when. The `ad_prefix` is used in some sort of generation of this ad.
```
schedule:
  - time: '2019-07-06T21:00:00'
    label: workoutWednesday
    ad_prefix: workout
```
