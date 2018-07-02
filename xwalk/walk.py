import yaml


VIEWER_COMMAND = [
    'led-image-viewer',
    '--led-cols=64',
    '--led-chain=2',
    '--led-no-hardware-pulse',
    '--led-gpio-mapping=adafruit-hat',
    '-L',
    '-R 270',
]


class AnimatedImage:
    """
    An instruction to show an animated image. The image may be played for a
    fixed number of loops and at a desired speed.
    """

    def __init__(self, path, loops=None, frame_delay=None):
        """Construct a new animated image step."""
        self.path = path
        self.loops = loops
        self.frame_delay = frame_delay

    def command(self):
        """Return a list of command line args for showing this image."""
        args = []
        args.extend(VIEWER_COMMAND)
        if self.loops:
            args.append("-l")
            args.append(self.loops)
        if self.frame_delay:
            args.append("-D")
            args.append(self.frame_delay)
        args.append(self.path)
        return " ".join(args)


class WalkScene:
    """
    A walk scene is a collection of an intro, walk, and outro animations with
    an optional audio file to play.
    """

    def __init__(self, intro, image, outro, audio=None):
        """Construct a new walk scene."""
        self.into = intro
        self.image = image
        self.outro = outro
        self.audio = audio

    def play_command(self):
        """Build command line for playing this scene in a shell."""
        # TODO: where to trigger audio?
        return " && ".join([img.command() for img in [self.intro, self.image, self.outro]])



### Scene Selection ###

class WalkSelector:
    """
    Walk selection logic provides a new walk scene on demand in response to the
    crosswalk button being pressed.
    """

    def choose_scene(self):
        raise "Abstract method choose_scene must be overridden by child classes"


class WeightedSceneTable(SceneSelector):
    """
    Randomly selects scenes from a weighted probability table.
    """

    def __init__(self, table):
        self.xxx = 123

    def choose_scene(self):
        pass


class CalendarSelector(SceneSelector):
    """
    Randomly selects scenes from a weighted probability table.
    """

    def __init__(self, rules):
        self.rules = rules

    def choose_scene(self):
        pass



### Data Loading ###

def from_yaml(filename):
    with open(filename) as f:
        raw_scenes = yaml.load(f)

    return {name: BasicScene(name, [AnimatedImage(**animation) for animation in animations]) for name, animations in raw_scenes.items()}

    # @staticmethod
    # def from_yaml(filename, image_path=""):
    #     """Load a collection of demos from a YAML file."""
    #     with open(filename) as f:
    #         demo_data = yaml.load(f)
    #     desc = data['desc']
    #     ppm = data['ppm'] in ['true', 'True']
    #     image = data['image'] && os.path.join(image_path, data['image'])
    #     return [LEDDemo(desc, ppm, image) for data in demo_data]
