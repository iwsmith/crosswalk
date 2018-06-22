import copy
import os
import random
import subprocess
import logging

DEMO_ARGS = ['demo', '--led-cols=64', '--led-chain=2', '-L', '-D']
IMG_VIEWER_ARGS = ['led-image-viewer', '--led-cols=64', '--led-no-hardware-pulse', '--led-chain=2', '--led-gpio-mapping=adafruit-hat', '-L', '-R 270']


DEMOS = ["some rotating square",
         "forward scrolling an image",
         "backward scrolling an image",
         "test image: a square",
         "Pulsing color",
         "Grayscale Block",
         "Abelian sandpile model",
         "Conway's game of life",
         "Langton's ant",
         "Volume bars",
         "Evolution of color",
         "Brightness pulse generator"]


class LEDController:
    def __init__(self, image_path):
        self.image_path = image_path
        self._process = None
        self._current_mode = "Off"

    def make_animation(self, animation):
        return ["-l", str(animation.loops), "-D", str(animation.frame_delay), os.path.join(self.image_path, animation.filename)]

    def scene(self, scene):
        args = copy.copy(IMG_VIEWER_ARGS)
        for animation in scene:
            args.extend(self.make_animation(animation))

        args.append("&&")
        args.extend(IMG_VIEWER_ARGS)
        args.extend(self.make_animation(scene.final))
        self._exec(" ".join(args), shell=True)
        self._current_mode = str(scene)

    def kill(self):
        self._current_mode = "Off"
        if self._process:
            subprocess.call(['pkill', '-P', self._process.pid])
            self._process.kill()
            self._process = None

    def demo(self, n, f=None):
        if n < 0 or n > 11:
            raise ValueError("Demo must be between 0 and 11.")

        args = copy.copy(DEMO_ARGS)
        args.append(str(n))

        if n is 1 or n is 2:
            if not f:
                raise ValueError("An .ppm must be provided when running demo 1 or 2.")
            args.append(os.path.join(self.image_path, f))

        self._exec(args)
        if f:
            self._current_mode = "Demo: " + DEMOS[n] + " - " + f
        else:
            self._current_mode = "Demo: " + DEMOS[n]

    def image(self, filename):
        args = copy.copy(IMG_VIEWER_ARGS)
        args.append(os.path.join(self.image_path, filename))

        self._exec(args)
        self._current_mode = "Image: " + filename

    def _exec(self, args, shell=False):
        self.kill()
        self._process = subprocess.Popen(args, shell=shell)

    def list_images(self):
        return os.listdir(self.image_path)

    def list_demos(self):
        return DEMOS

    def random_image(self):
        return self.image(random.choice(self.list_images()))

    def status(self):
        return str(self)

    def __str__(self):
        return "LEDController: " + self._current_mode


class MockController(LEDController):
    def __init__(self, image_path):
        LEDController.__init__(self, image_path)

    def _exec(self, args, shell=False):
        self.kill()
        logging.info(args)
        self._process = args

    def kill(self):
        self._current_mode = "Off"
        if self._process:
            logging.info("Kill" + str(self._process))
            self._process = None

    def __str__(self):
        return "MockController: " + self._current_mode + str(self._process)

