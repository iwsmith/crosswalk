import os
import random
import yaml


class Animation:
    """
    An instruction to show an animated image. The image may be played for a
    fixed number of loops and at a desired speed, and have an audio file
    associated with it.
    """

    def __init__(self, name, image_path, audio_path=None, loops=None, frame_delay=None):
        """Construct a new animated image step."""
        self.name = name
        self.image_path = image_path
        self.audio_path = audio_path
        self.loops = loops
        self.frame_delay = frame_delay


    def __str__(self):
        """Render the animation as a string."""
        return "Animation {}: {}{}".format(
            self.name,
            self.image_path,
            " ({})".format(self.audio_path) if self.audio_path else "")


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


class Library:
    """
    A library of animations, used to construct new scenes.
    """

    def __init__(self, image_dir, audio_dir, config_path):
        self.image_dir = image_dir
        self.audio_dir = audio_dir
        self.config_path = config_path
        self.intros = []
        self.outros = []
        self.walks = []
        self.uploads = []
        self.refresh()


    def _load_images(self, namespace, config={}, sounds={}, default_sound=None):
        """Load a directory of images, returning a list of animations."""
        animations = []
        for filename in os.listdir(os.path.join(self.image_dir, namespace)):
            name = os.path.splitext(filename)[0]
            path = os.path.join(self.image_dir, namespace, filename)
            cfg = config.get(namespace, {}).get(name, {})
            animation = Animation(name, path)

            if 'loops' in cfg:
                animation.loops = cfg['loops']

            if 'frame_delay' in cfg:
                animation.frame_delay = cfg['frame_delay']

            if 'audio' in cfg:
                animation.audio_path = os.path.join(self.audio_dir, cfg['audio'])
            elif name in sounds:
                animation.audio_path = sounds[name]
            elif default_sound is not None:
                animation.audio_path = os.path.join(self.audio_dir, default_sound)

            animations.append(animation)

        return animations


    def refresh(self):
        """Rescan the files available and reload the configuration."""
        try:
            with open(self.config_path) as f:
                config = yaml.load(f)
        except Error:
            config = {}

        sounds = {
            os.path.splitext(filename)[0]: os.path.join(self.audio_dir, filename)
            for filename in os.listdir(self.audio_dir)
        }

        self.intros = self._load_images('intros', config, sounds)
        self.outros = self._load_images('outros', config, sounds)
        self.walks = self._load_images('walks', config, sounds, 'walk_now.wav')
        self.uploads = self._load_images('uploads')


    def choose_walk(self):
        """
        Generate a new walk scene by selecting from the available intros,
        walks, and outros.
        """
        # TODO: implement
        pass

    # ...
