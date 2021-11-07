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
        self.menu = []
        self.refresh()


    def _load_images(self, namespace, config={}, sounds={}, default_sound=None, default_loops=1):
        """Load a directory of images, returning a list of animations."""
        animations = []
        subdir = os.path.join(self.image_dir, namespace)
        logger.debug("Loading %s images in %s", namespace, subdir)
        for filename in os.listdir(subdir):
            name, ext = os.path.splitext(filename)

            if ext:
                path = os.path.join(subdir, filename)
                cfg = (config.get(namespace) or {}).get(name, {})
                animation = Animation(name, path)
                animation.category = cfg.get('category')
                animation.frame_delay = cfg.get('frame_delay')
                animation.loops = cfg.get('loops', default_loops)
                animation.skip_intro = cfg.get('skip_intro', False)
                animation.skip_outro = cfg.get('skip_outro', False)

                if 'audio' in cfg:
                    animation.audio_path = os.path.join(self.audio_dir, cfg['audio'])
                elif name in sounds:
                    animation.audio_path = sounds[name]
                elif default_sound is not None:
                    animation.audio_path = os.path.join(self.audio_dir, default_sound)

                if not animation.category:
                    logger.warning("No category found for %s", filename)

                animations.append(animation)

        categories = set([animation.category for animation in animations if animation.category])
        logger.info("Loaded %d images across categories: %s", len(animations), ", ".join(categories))

        return sorted(animations, key=lambda x: x.name)


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
        self.walks = self._load_images('walks', config, sounds, 'walk_now.wav', 5)
        self.ads = self._load_images('ads', config, sounds, default_loops=None)

        self.weights = config['weights'] or {}
        self.menu = [
            {
                'start': datetime.strptime(entry['start'], "%Y-%m-%dT%H:%M:%S"),
                'weights': entry['weights'],
            }
            for entry in config['menu']
        ]


    def find_image(self, name, coll=None):
        """Look for an image by name in the walks and uploads folders."""
        if coll is None:
            coll = self.walks + self.uploads

        for animation in coll:
            if animation.name == name:
                return animation


    def find_scene(self, image_names):
        """
        Build a scene attempting to match the given intro, walk, and outro
        names. This is used for synchronizing with the choices made by the other
        sign.
        """
        intro_name, walk_name, outro_name = image_names
        intro = next(image for image in self.intros if image.name == intro_name) if intro_name else None
        outro = next(image for image in self.outros if image.name == outro_name) if outro_name else None
        walk = next(image for image in self.walks if image.name == walk_name)
        return Scene([intro, walk, outro])


    def _menu_entry(self, time=None):
        """
        Search through the menu looking at the start dates. Returns the last
        entry which is earlier than the given time.
        """
        # Nothing to pick if menu is empty.
        if not self.menu:
            return None
        time = time or datetime.now()
        recent = self.menu[0]
        for entry in self.menu:
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
        current = self._menu_entry()
        valid_categories = set([animation.category for animation in self.walks if animation.category])

        weight_name = current and current.get('weights')
        weights = weight_name and self.weights.get(weight_name) or {}
        weights = {
            category: weight
            for category, weight in weights.items()
            if category in valid_categories
        }
        logger.debug("Currently scheduled menu entry %s resulted in pruned weight table: %s", current, repr(weights))

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


    def build_scene(self, walk=None, exclude=[]):
        """
        Generate a new walk scene by selecting from the available intros,
        walks, and outros. A specific walk name may be provided to force its
        selection.
        """
        # Select a random intro if not skipped.
        intro = None
        if walk is None or not walk.skip_intro:
            intro = random.choice(self.intros)

        # Select a random outro if not skipped.
        outro = None
        if walk is None or not walk.skip_outro:
            outro = random.choice(self.outros)

        # Select a walk by randomly choosing from the weighted menu.
        if walk is None:
            for attempt in range(10):
                walk = self._choose_walk()
                if walk in exclude:
                    logger.debug("Skipping walk %s which is in exclusions %s", walk.name, [animation.name for animation in exclude])
                else:
                    break
            logger.info("Randomly selected walk %s", walk)
        else:
            logger.info("Force selected walk %s", walk)

        return Scene([intro, walk, outro])
