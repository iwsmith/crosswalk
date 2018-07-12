from datetime import datetime, timedelta
import logging
import os

import requests

from xwalk.animation import Animation, Scene, Library
from xwalk.audio import AudioController
from xwalk.demo import DemoController
from xwalk.image import ImageController


logger = logging.getLogger(__name__)


class CrossWalk:
    """
    Core crossXwalk logic engine.
    """

    def __init__(self, library, log_file='walks.tsv'):
        with open('/etc/hostname') as f:
            self.host = f.read().rstrip()
        self._log_file = log_file
        self.library = library
        self.demos = DemoController()
        self.image = ImageController()
        self.audio = AudioController()
        self.halt = Animation('halt', os.path.join(library.image_dir, 'stop.gif'))
        self.mode = 'off'
        self.cooldown = 17
        self.queue = []
        self.history = []
        self.ready = True


    def make_ready(self):
        """Sets the crosswalk to ready"""
        if self.ready:
            logger.warn('Trying to set crosswalk to ready, it is already ready')
        self.ready = True


    def is_ready(self):
        """True if the crosswalk is ready for a button press."""
        return self.ready


    def state(self):
        """Return the crosswalk state."""
        return {
            'host': self.host,
            'mode': self.mode,
            'demo': self.demos.playing(),
            'image': self.image.playing(),
            'audio': self.audio.playing(),
            'queue': [walk.name for walk in self.queue],
            'history': [walk.name for walk in self.history],
            'cooldown': self.cooldown,
            'ready': self.is_ready(),
        }


    def off(self):
        """Set the crosswalk mode to 'off'."""
        self.demos.kill()
        self.image.kill()
        self.audio.kill()
        self.mode = 'off'


    def demo(self, demo_id):
        """Set the crosswalk mode to play a demo."""
        self.image.kill()
        self.audio.kill()
        self.demos.play(demo_id)
        self.mode = 'demo'


    def show(self, animation):
        """Set the crosswalk mode to show an image."""
        self.demos.kill()
        animation = animation.copy()
        animation.loops = None
        if animation.audio_path:
            self.audio.play(animation)
        else:
            self.audio.kill()
        self.image.play(animation)
        self.mode = 'image'


    def walk(self):
        """Set the crosswalk to walk mode."""
        self.demos.kill()
        self.audio.kill()
        self.make_ready()
        self.image.play(self.halt)
        self.mode = 'walk'


    def _play_walk(self, tag, scene):
        """Play a walk scene."""
        intro, walk, outro = scene
        scene.append(self.halt)
        self.demos.kill()
        self.ready = False
        self.image.play_all(scene)
        self.audio.play_all(scene)
        if len(self.history) >= 50:
            self.history = self.history[1:50]
        self.history.append(walk)
        with open(self._log_file, 'a') as log:
            log.write("{}\t{}\t{}\n".format(datetime.now(), tag, walk.name))


    def sync(self, image_names):
        """
        Synchronize this crosswalk with an animation scene selected by the
        other sign.
        """
        if self.mode != 'walk':
            logger.warn("Ignoring sync call while in non-walk mode")
        elif self.is_ready():
            pass
        elif self.host == 'crosswalk-a':
            logger.warn("Ignoring contentious sync call while on cooldown")
            return
        else:
            logger.warn("Overriding cooldown state for contentious sync call")
        scene = self.library.find_scene(image_names)
        self._play_walk('sync', scene)


    def button(self, hold=0.0):
        """
        Indicate that a button has been pressed. If 'hold' is set, it means the
        button was held down for at least that many seconds.
        """
        logger.debug("Button press: %.1f s", hold)
        if self.mode == 'off':
            # TODO: if long press, switch to next on mode
            pass
        elif self.mode == 'demo':
            # TODO: if long press, switch off
            self.demos.next()
        elif self.mode == 'image':
            # TODO: if long press, switch off
            # TODO: show next image
            pass
        elif self.mode == 'walk':
            # TODO: if long press, switch off
            if self.is_ready():
                if self.queue:
                    next_walk = self.queue.pop(0)
                    scene = self.library.build_scene(walk=next_walk)
                    tag = 'queue'
                else:
                    scene = self.library.build_scene(exclude=self.history[-3:])
                    tag = 'random'
                logger.info("Selected scene: %s", scene)
                dual = 'crosswalk-b' if self.host == 'crosswalk-a' else 'crosswalk-a'
                try:
                    requests.post("http://{}/sync".format(dual), json={'scene': [animation.name for animation in scene]})
                except Exception as ex:
                    logger.warn("Failed to synchronize with %s: %s", dual, ex)
                self._play_walk(tag, scene)
