import copy
import os
import random
import subprocess

DEMO_ARGS = ['demo', '--led-cols=64', '--led-chain=2', '-L', '-D']
IMG_VIEWER_ARGS = ['led-image-viewer', '--led-cols=64', '--led-no-hardware-pulse', '--led-chain=2', '--led-gpio-mapping=adafruit-hat', '-L', '-R 270']


DEMOS = ["some rotating square",
         "forward scrolling an image",
         "backward scrolling an image",
         "test image: a square",
         "Pulsing color",
         "Grayscale Block",
         "Abelian sandpile model",
         "Conway 's game of life",
         "Langton 's ant",
         "Volume bars",
         "Evolution of color",
         "Brightness pulse generator"]


class LEDController:
    def __init__(self, image_path):
        self.image_path = image_path
        self.__process = None
        self._current_mode = "Off"

    def kill(self):
        self._current_mode = "Off"
        if self.__process:
            self.__process.kill()
            self.__process = None

    def demo(self, n, f=None):
        if n < 0 or n > 11:
            raise ValueError("Demo must be between 0 and 11.")

        args = copy.copy(DEMO_ARGS)
        args.append(str(n))

        if n is 1 or n is 2:
            if not f:
                raise ValueError("An .ppm must be provided when running demo 1 or 2.")
            args.append(os.path.join(self.image_path, f))

        self._current_mode = "Demo " + n + f
        self.__exec(args)

    def image(self, filename):
        args = copy.copy(IMG_VIEWER_ARGS)
        args.append(os.path.join(self.image_path, filename))

        self._current_mode = "Image " + filename
        self.__exec(args)

    def __exec(self, args):
        self.kill()
        self.__process = subprocess.Popen(args)

    def list_images(self):
        return os.listdir(self.image_path)

    def list_demos(self):
        return DEMOS

    def random_image(self):
        return self.image(random.choice(self.list_images()))

    def __str__(self):
        return "LEDController: " + self._current_mode



