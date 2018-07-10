from datetime import datetime
import logging
import os
import random
import yaml

logger = logging.getLogger(__name__)


class Animation:
    """
    An instruction to show an animated image. The image may be played for a
    fixed number of loops and at a desired speed, and have an audio file
    associated with it.
    """

    def __init__(
            self, name, image_path,
            audio_path=None,
            frame_delay=None,
            loops=None,
            category=None):
        """Construct a new animated image step."""
        self.name = name
        self.image_path = image_path
        self.audio_path = audio_path
        self.frame_delay = frame_delay
        self.loops = loops
        self.category = category


    def __str__(self):
        """Render the animation as a string."""
        return "Animation {}: {}{}".format(
            self.name,
            self.image_path,
            " ({})".format(self.audio_path) if self.audio_path else "")


    def copy(self):
        """Return a copy of this animation."""
        return Animation(
            self.name,
            self.image_path,
            self.audio_path,
            self.loops,
            self.frame_delay)


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


    def __str__(self):
        """Render the scene as a string."""
        return "Scene {}".format([image.name for image in self.animations])


    def append(self, animation):
        """Add an animation to this scene.."""
        self.animations.append(animation)
        return self


class Library:
    """
    A library of animations, used to construct new scenes.
    """

    def __init__(self, config_path, image_dir, audio_dir):
        self.config_path = config_path
        self.image_dir = image_dir
        self.audio_dir = audio_dir
        self.intros = []
        self.outros = []
        self.walks = []
        self.uploads = []
        self.weights = {}
        self.schedule = []
        self.refresh()


    def _load_images(self, namespace, config={}, sounds={}, default_sound=None):
        """Load a directory of images, returning a list of animations."""
        animations = []
        subdir = os.path.join(self.image_dir, namespace)
        logger.debug("Loading %s images in %s", namespace, subdir)
        for filename in os.listdir(subdir):
            name = os.path.splitext(filename)[0]
            path = os.path.join(subdir, filename)
            cfg = (config.get(namespace) or {}).get(name, {})
            animation = Animation(name, path)
            animation.category = cfg.get('category')
            animation.frame_delay = cfg.get('frame_delay')
            animation.loops = cfg.get('loops', 1)

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

        self.uploads = self._load_images('uploads')
        self.intros = self._load_images('intros', config, sounds)
        self.outros = self._load_images('outros', config, sounds)
        self.walks = self._load_images('walks', config, sounds)

        self.weights = config['weights'] or {}
        self.schedule = [
            {
                'start': datetime.strptime(entry['start'], "%Y-%m-%dT%H:%M:%S"),
                'weights': entry['weights'],
            }
            for entry in config['schedule']
        ]


    def find_image(self, name):
        """Look for an image by name in the walks and uploads folders."""
        for animation in self.walks + self.uploads:
            if animation.name == name:
                return animation


    def find_scene(self, image_names):
        """
        Build a scene attempting to match the given intro, walk, and outro
        names.
        """
        intro_name, walk_name, outro_name = image_names
        intro = next(image for image in self.intros if image.name == intro_name)
        outro = next(image for image in self.outros if image.name == outro_name)
        walk = next(image for image in self.walks if image.name == walk_name)
        return Scene([intro, walk, outro])


    def _scheduled_entry(self, time=datetime.now()):
        """
        Search through the schedule looking at the start dates. Returns the last
        entry which is earlier than the given time.
        """
        # Nothing to pick if schedule is empty.
        if not self.schedule:
            return None
        recent = self.schedule[0]
        for entry in self.schedule:
            start = entry.get('start')
            if start is None or time < start:
                break
            recent = entry
        return recent


    def _choose_walk(self):
        """
        Generate a new walk scene by selecting from the available intros,
        walks, and outros.
        """
        current = self._scheduled_entry()
        valid_categories = set([animation.category for animation in self.walks if animation.category])

        weight_name = current and current.get('weights')
        weights = weight_name and self.weights.get(weight_name) or {}
        weights = {
            category: weight
            for category, weight in weights.items()
            if category in valid_categories
        }
        logger.debug("Currently scheduled entry %s resulted in pruned weight table: %s", current, repr(weights))

        # Uniform random if no (or empty) weight table.
        if not weights:
            return random.choice(self.walks)

        # Find which category our random dart lands on.
        total = sum(weights.values())
        point = random.randrange(0, total)
        for category, weight in weights.items():
            selected = category
            point -= weight
            if point <= 0:
                break
        # Pick a random image from the category.
        return random.choice([
            animation
            for animation in self.walks
            if selected == '_' and animation.category not in weights or animation.category == selected
        ])


    def build_scene(self, walk=None):
        """
        Generate a new walk scene by selecting from the available intros,
        walks, and outros. A specific walk name may be provided to force its
        selection.
        """
        intro = random.choice(self.intros)
        outro = random.choice(self.outros)
        if walk is None:
            walk = self._choose_walk()
            logger.info("Randomly selected walk %s", walk)
        else:
            logger.info("Force selected walk %s", walk)
        return Scene([intro, walk, outro])
