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
            args.append(str(animation.loops))
        if animation.frame_delay:
            args.append("-D")
            args.append(str(animation.frame_delay))
        args.append(animation.image_path)
        return args


    def _done_command(self):
        return "/usr/bin/curl http://localhost/ready"


    def playing(self):
        """Return a vector of information about the currently playing animations."""
        return [str(animation) for animation in self._playing or []]


    def kill(self):
        """Kill the currently playing animation, if any."""
        if self._process:
            #logger.debug("Killing: %s", self.playing())
            subprocess.call(['/usr/bin/pkill', '-P', str(self._process.pid)])
            self._process.kill()
            self._process = None
        self._playing = None


    def _exec(self, command, shell=False):
        """Execute a new subprocess command."""
        self.kill()
        logger.debug("Executing: %s", command)
        self._process = subprocess.Popen(command, shell=shell)


    def play(self, animation):
        """
        Play the given animation. Any currently playing image will be replaced.
        """
        self.kill()

        if animation is None:
            return

        command = self._display_command(animation)

        logger.info("Playing: %s", animation)
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

        # Hit the done endpoint so we know we are done
        commands.insert(-1, self._done_command())
        script = " && ".join(commands)

        logger.info("Playing all: %s", [image.name for image in animations])
        logger.info("Script: %s", script)
        self._exec(script, shell=True)
        self._playing = animations
