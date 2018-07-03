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
        self.demos = {
            i, LEDDemo(i, desc, i in [1, 2])
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


    def play(demo_id, image=None):
        """
        Play the demo with the given identifier, if available in the
        controller. Any currently playing demo will be replaced.
        """
        if demo_id not in self.demos:
            raise ValueError("Demo id must be in {}".format(self.demos.keys()))
        demo = self.demos[demo_id]

        args = []
        args.extend(DEMO_COMMAND)
        args.append(str(demo.demo_id))

        if demo.ppm_required:
            if image is None:
                raise ValueError("A .ppm image must be provided for demo {}".format(demo.demo_id))
            args.append(image)

        self.kill()
        self._process = subprocess.Popen(args)
        self._playing = demo_id


    def kill(self):
        """Kill the currently running demo, if any."""
        self._playing = None
        if self._process:
            #subprocess.call(['/usr/bin/pkill', '-P', str(self._process.pid)])
            self._process.kill()
            self._process = None
