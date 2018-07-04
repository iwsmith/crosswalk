# Basic animation classes.

class Animation:
    """
    An instruction to show an animated image. The image may be played for a
    fixed number of loops and at a desired speed, and have an audio file
    associated with it.
    """

    def __init__(self, image_path, audio_path=None, loops=None, frame_delay=None):
        """Construct a new animated image step."""
        self.image_path = image_path
        self.audio_path = audio_path
        self.loops = loops
        self.frame_delay = frame_delay


class Scene:
    """
    A scene is a sequence of animations.
    """

    def __init__(self, animations):
        """Construct a new scene from the given animations."""
        self.animations = animations


    def __iter__(self):
        """Iterate through the animations in this scene."""
        return iter(self.animations)


    def extend(self, more):
        """Extend this scene with more animations. Mutates the scene."""
        self.animations.extend(more)
        return self
