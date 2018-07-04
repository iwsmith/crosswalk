import logging
import subprocess


DEMO_COMMAND = [
    'demo',
    '--led-cols=64',
    '--led-chain=2',
    '-L',
    '-D',
]


class LEDDemo:
    """
    Represents a demo shipped with the Adafruit LED controller drivers.
    """

    def __init__(self, demo_id, description, ppm_required=False):
        """Initialize a new demo record."""
        self.demo_id = demo_id
        self.description = description
        self.ppm_required = ppm_required


class DemoController:
    """
    Controller to drive the LED panels with a demo program.
    """

    def __init__(self):
        """Construct a new demo controller."""
        self._process = None
        self._playing = None
        self._demos = {
            i: LEDDemo(i, desc, i in [1, 2])
            for i, desc in enumerate([
                "Rotating Square",
                "Forward Scrolling Image",
                "Backward Scrolling Image",
                "Test Color Square",
                "Pulsing Color",
                "Grayscale Block",
                "Abelian Sandpile",
                "Conway's Game of Life",
                "Langton's Ant",
                "Volume Bars",
                "Evolution of Color",
                "Brightness Pulse Generator",
            ])
        }


    def list_demos(self):
        """Return a list of the available demos to play."""
        return self._demos.values()


    def kill(self):
        """Kill the currently running demo, if any."""
        if self._process:
            logging.debug("Killing {}".format(self._playing))
            self._process.kill()
            self._process = None
        self._playing = None


    def _exec(self, command):
        """Execute the given command as a new subprocess."""
        self.kill()
        logging.debug(command)
        #self._process = subprocess.Popen(args)


    def play(self, demo_id, image=None):
        """
        Play the demo with the given identifier, if available in the
        controller. Any currently playing demo will be replaced.
        """
        if demo_id not in self._demos:
            raise ValueError("Demo id must be in {}".format(self._demos.keys()))
        demo = self._demos[demo_id]

        args = []
        args.extend(DEMO_COMMAND)
        args.append(str(demo.demo_id))

        if demo.ppm_required:
            if image is None:
                raise ValueError("A .ppm image must be provided for demo {}".format(demo.demo_id))
            args.append(image)

        logging.info("Playing {} ({})".format(demo.description, command))
        self._exec(args)
        self._playing = demo_id
