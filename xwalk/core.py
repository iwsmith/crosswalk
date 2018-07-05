from datetime import datetime, timedelta
import logging
import os

from xwalk.animation import Animation, Scene, Library
from xwalk.audio import AudioController
from xwalk.demo import DemoController
from xwalk.image import ImageController


logger = logging.getLogger(__name__)


class CrossWalk:
    """
    Core crossXwalk logic engine.
    """

    def __init__(self, library):
        with open('/etc/hostname') as f:
            self.host = f.read().rstrip()
        self.library = library
        self.demos = DemoController()
        self.image = ImageController()
        self.audio = AudioController()
        self.halt = Animation('halt', os.path.join(library.image_dir, 'stop.png'))
        self.mode = 'off'
        self.cooldown = 30
        self.ready_at = datetime.now()


    def is_ready(self):
        """True if the crosswalk is ready for a button press."""
        return self.ready_at <= datetime.now()


    def state(self):
        """Return the crosswalk state."""
        return {
            'host': self.host,
            'mode': self.mode,
            'demo': self.demos.playing(),
            'image': self.image.playing(),
            'audio': self.audio.playing(),
            'cooldown': self.cooldown,
            'ready_at': self.ready_at,
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
        self.image.play(self.halt)
        self.mode = 'walk'


    def _play_walk(self, scene):
        """Play a walk scene."""
        scene.append(self.halt)
        self.image.play_all(scene)
        self.audio.play_all(scene)
        self.ready_at = datetime.now() + timedelta(seconds=self.cooldown)


    def sync(self, intro_name, walk_name, outro_name):
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
        scene = self.library.find_scene(intro_name, walk_name, outro_name)
        self._play_walk(scene)


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
                # TODO: walk interaction
                # select a new walk scene
                scene = self.library.choose_walk()
                logger.info("Selected scene: %s", scene)
                # TODO: sync alternate crosswalk
                self._play_walk(scene)
