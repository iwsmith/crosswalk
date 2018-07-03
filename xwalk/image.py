import logging
import subprocess


VIEWER_COMMAND = [
    'led-image-viewer',
    '--led-cols=64',
    '--led-chain=2',
    '--led-no-hardware-pulse',
    '--led-gpio-mapping=adafruit-hat',
    '-L',
    '-R 270',
]


class Animation:
    """
    An instruction to show an animated image. The image may be played for a
    fixed number of loops and at a desired speed.
    """

    def __init__(self, path, loops=None, frame_delay=None):
        """Construct a new animated image step."""
        self.path = path
        self.loops = loops
        self.frame_delay = frame_delay


class ImageController:
    """
    Controller to drive the LED panels with an animated image.
    """

    def __init__(self):
        """Construct a new image controller."""
        self._process = None
        self._playing = None


    def _display_command(self, animation):
        """
        Return a list of command line arguments for showing the animated image.
        """
        args = []
        args.extend(VIEWER_COMMAND)
        if animation.loops:
            args.append("-l")
            args.append(animation.loops)
        if animation.frame_delay:
            args.append("-D")
            args.append(animation.frame_delay)
        args.append(animation.path)
        return args


    def kill(self):
        """Kill the currently playing animation, if any."""
        logging.debug("Killing " + self._playing)
        if self._process:
            subprocess.call(['/usr/bin/pkill', '-P', str(self._process.pid)])
            self._process.kill()
            self._process = None
        self._playing = None


    def play(self, animation):
        """
        Play the given animation. Any currently playing image will be replaced.
        """
        self.kill()

        if animation is None:
            return

        command = self._display_command(animation)
        logging.debug("Playing {} ({})".format(animation, command))

        self._process = subprocess.Popen(command)
        self._playing = [animation]


    def play_all(self, animations):
        """
        Play the given animations in sequence. Any currently playing image will
        be replaced.
        """
        self.kill()

        if not animations:
            return

        commands = [" ".join(self._display_command(animation)) for animation in animations]
        script = " && ".join(commands)
        logging.debug("Playing all {} ({})".format(animations, script))

        self._process = subprocess.Popen(script, shell=True)
        self._playing = animations
