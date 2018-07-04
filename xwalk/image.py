import logging
import subprocess

import xwalk.scene


VIEWER_COMMAND = [
    'led-image-viewer',
    '--led-cols=64',
    '--led-chain=2',
    '--led-no-hardware-pulse',
    '--led-gpio-mapping=adafruit-hat',
    '-L',
    '-R 270',
]

logger = logging.getLogger(__name__)


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


    def playing(self):
        """Return a vector of information about the currently playing animations."""
        return [str(animation) for animation in self._playing or []]


    def kill(self):
        """Kill the currently playing animation, if any."""
        if self._process:
            logger.debug("Killing {}".format(self._playing))
            subprocess.call(['/usr/bin/pkill', '-P', str(self._process.pid)])
            self._process.kill()
            self._process = None
        self._playing = None


    def _exec(self, command, shell=False):
        """Execute a new subprocess command."""
        self.kill()
        logger.debug(command)
        #self._process = subprocess.Popen(args, shell=shell)


    def play(self, animation):
        """
        Play the given animation. Any currently playing image will be replaced.
        """
        self.kill()

        if animation is None:
            return

        command = self._display_command(animation)

        logger.info("Playing {} ({})".format(animation, " ".join(command)))
        self._exec(command)
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

        logger.info("Playing all {} ({})".format(animations, script))
        self._exec(script, shell=True)
        self._playing = animations
