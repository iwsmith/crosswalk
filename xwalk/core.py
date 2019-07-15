from datetime import datetime, timedelta
import logging
import subprocess
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

    def __init__(self, library, schedule, log_file='walks.tsv'):
        with open('/etc/hostname') as f:
            self.host = f.read().rstrip()
        self._log_file = log_file
        self.library = library
        self.schedule = schedule
        self.demos = DemoController()
        self.image = ImageController()
        self.audio = AudioController()
        self.base_halt = Animation('halt', os.path.join(library.image_dir, 'stop.gif'))
        self.last_halt = None
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
            'now': str(datetime.now()),
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
        halt = self._halt_image()
        self.last_halt = halt.image_path
        self.image.play(halt)
        self.mode = 'walk'


    def _play_walk(self, tag, scene):
        """Play a walk scene."""
        intro, walk, outro = scene
        halt = self._halt_image()
        self.last_halt = halt.image_path
        scene.append(halt)
        self.demos.kill()
        self.ready = False
        self.image.play_all(scene)
        self.audio.play_all(scene)
        if len(self.history) >= 50:
            self.history = self.history[1:50]
        self.history.append(walk)
        with open(self._log_file, 'a') as log:
            log.write("{}\t{}\t{}\n".format(datetime.now(), tag, walk.name))


    def _halt_image(self):
        """Return the halt image to use when between walks."""
        ad_image = None

        # See if we're within a certain period of the next event and if that
        # event has a custom halt advertisement.
        next_event = self.schedule.next_event(before=(datetime.now() + timedelta(hours=1)))
        if next_event and next_event.ad_prefix:
            ad_image = self.library.find_image(next_event.current_ad(), self.library.ads)

        return ad_image or self.base_halt


    def sync(self, image_names, event_key=None):
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

        # If the other crosswalk is initiating an event, take it off of the
        # local schedule.
        if event_key:
            self.schedule.advance(event_key)

        # Locate and play the walk scene.
        scene = self.library.find_scene(image_names)
        self._play_walk('sync', scene)


    def tick(self, now=None):
        """Handle periodic tasks and updating the current time."""
        # If remote clock is far ahead of this one, fast forward.
        if now is not None:
            remote_now = datetime.fromtimestamp(now)
            local_now = datetime.now()
            skew = (remote_now - local_now).total_seconds()
            if 60 <= skew:
                logger.warn("Fast-forwarding clock to %s", now)
                subprocess.Popen("date " + now.strftime("%m%d%H%M%Y.%S"))
        # Check if halt image should be changed.
        if self.mode == 'walk' and self.ready:
            halt = self._halt_image()
            if halt.image_path != self.last_halt:
                self.last_halt = halt.image_path
                self.image.play(halt)
        return {"tock": True}


    def _walk_button(self):
        """
        What to do when the button is pressed in walk mode.
        """
        # Bail if the crosswalk is not ready.
        if not self.is_ready():
            return

        # If the next scheduled event is in the _past_ we had it queued
        # up and should play the event now.
        next_event = self.schedule.next_event()
        if next_event:
            logger.debug("Playing scheduled event %s: %s", next_event.label, next_event)
            self.schedule.advance()
            # TODO: custom intro or skip intro?
            walk = self.library.find_image(next_event.image)
            scene = self.library.build_scene(walk=walk)
            tag = 'event'

        # If there are walks queued up, play the next one.
        elif self.queue:
            next_walk = self.queue.pop(0)
            scene = self.library.build_scene(walk=next_walk)
            tag = 'queue'

        # Otherwise randomly pick a walk.
        else:
            scene = self.library.build_scene(exclude=self.history[-3:])
            tag = 'random'

        logger.info("Selected scene: %s", scene)

        # Sync selection with the other crosswalk.
        dual = 'crosswalk-b' if self.host == 'crosswalk-a' else 'crosswalk-a'
        try:
            req = {
                'now': datetime.now().timestamp(),
                'scene': [animation.name for animation in scene],
            }
            if tag == 'event':
                req['event'] = next_event.event_key()
            requests.post("http://{}/sync".format(dual), json=req)
        except Exception as ex:
            logger.warn("Failed to synchronize with %s: %s", dual, ex)

        # Play the selected scene.
        self._play_walk(tag, scene)


    def button(self, hold=0.0):
        """
        Indicate that a button has been pressed. If 'hold' is set, it means the
        button was held down for at least that many seconds.
        """
        long_press = (10.0 <= hold)
        logger.debug("Button %s press: %.1f s", 'long' if long_press else 'short', hold)
        if self.mode == 'off':
            # IDEA: short press could cycle between 'on' modes and show a mode
            # name on the screen for a short time, then long press activates
            # that mode?
            if long_press:
                self.walk()
        elif self.mode == 'demo':
            if long_press:
                self.off()
            else:
                self.demos.next()
        elif self.mode == 'image':
            if long_press:
                self.off()
        elif self.mode == 'walk':
            if long_press:
                self.off()
            else:
                self._walk_button()
