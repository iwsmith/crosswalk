# Demo

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

    def command(self, image=None):
        """Return the command line args for rendering this demo."""
        args = []
        args.extend(DEMO_COMMAND)
        args.append(str(self.demo_id))

        if self.ppm_required:
            if image is None:
                raise ValueError("A .ppm image must be provided")
            args.append(self.image)

        return args


DEMOS = [
    LEDDemo(i, desc, i in [1, 2])
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
]
