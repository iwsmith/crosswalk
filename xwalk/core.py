from datetime import datetime
import os

from xwalk.audio import AudioController
from xwalk.demo import DemoController
from xwalk.image import ImageController
from xwalk.scene import Animation, Scene



class CrossWalk:
    """
    Core crossXwalk logic engine.
    """

    def __init__(self, image_dir, audio_dir):
        self.demos = DemoController()
        self.image = ImageController()
        self.audio = AudioController()
        self.mode = 'off'
        self.halt = Animation(os.path.join(image_dir, 'stop.png'))
        self.cooldown = 30
        self.ready_at = datetime.now()

        # TODO: load images and audio independently from controllers.


    def is_ready(self):
        """True if the crosswalk is ready for a button press."""
        return self.ready_at <= datetime.now()


    def state(self):
        """Return the crosswalk state."""
        return {
            'mode': self.mode,
            'demo': self.demos._playing,
            'image': self.image._playing,
            'audio': self.audio._playing,
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


    def image(self, animation):
        """Set the crosswalk mode to show an image."""
        self.demos.kill()
        self.audio.kill()
        self.image.play(animation)
        self.mode = 'image'


    def walk(self):
        """Set the crosswalk to walk mode."""
        self.demos.kill()
        self.audio.kill()
        self.image.play(self.halt)
        self.mode = 'walk'


    def button(self, hold=0.0):
        """
        Indicate that a button has been pressed. If 'hold' is set, it means the
        button was held down for at least that many seconds.
        """
        # TODO: things
        pass