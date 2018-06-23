import yaml


class AnimatedImage:
    def __init__(self, filename, loops=-1, frame_delay=-1):
        self.filename = filename
        self.loops = loops
        self.frame_delay = frame_delay


class BasicScene:
    def __init__(self, name, animations):
        self.name = name

        self.final = animations.pop()

        self.animations = animations

    def __iter__(self):
        return iter(self.animations)

    def __str__(self):
        return "BasicScene " + self.name + ": " + str(len(self.animations) + 1) + " animations"


def from_yaml(filename):
    with open(filename) as f:
        raw_scenes = yaml.load(f)

    return {name: BasicScene(name, [AnimatedImage(**animation) for animation in animations]) for name, animations in raw_scenes.items()}


