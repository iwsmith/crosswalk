## Installation
1. Install the [Ada Fruit Drivers](https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi/driving-matrices)
2. Build the utils in `./rpi-rgb-led-matrix/utils`
3. Add `led-image-viewer` and `demo` to your `PATH`
4. `sudo apt-get install python3-flask`

## Running
1. As **root** `FLASK_APP=run.py  flask run --host=0.0.0.0`

## Content
### Creating New Voice Commands
On a Mac `say -v Samantha "Walk Sign Is On. Walk Now." --data-format=LEF32@22050 -o walk_now.wav` 
