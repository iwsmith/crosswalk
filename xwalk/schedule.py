from datetime import datetime, timedelta
import logging
import os
import yaml

logger = logging.getLogger(__name__)


def format_event_key(label, time):
    """Generate a new event key based on the label and time."""
    return "{}|{}".format(label, time)


class Event:
    """
    A scheduled event.
    """

    def __init__(self, label, time, image, audio, ad_prefix=None):
        """Construct a new schedule event."""
        self.label = label
        self.time = time
        self.image = image
        self.audio = audio
        self.ad_prefix = ad_prefix


    def event_key(self):
        """Return a key identifying this event."""
        return format_event_key(self.label, self.time)


    def current_ad(self, time=datetime.now()):
        """
        Return the current advertisement image path based on the number of
        minutes between now and the event start.
        """
        if self.ad_prefix is None:
            return None

        pending = (self.time - time).total_seconds()
        current = None

        # Find the *last* entry which is greater than the pending time.
        for minutes in [60, 45, 30, 15, 10, 5, 0]:
            if pending <= minutes:
                current = minutes

        # Construct the ad image name.
        if current is None:
            return None
        elif current == 0:
            return '{}-start.gif'.format(self.ad_prefix)
        else:
            return '{}-{}m.gif'.format(self.ad_prefix, current)


class Schedule:
    """
    A schedule of events to play at specific times.
    """

    def __init__(self, config_path):
        self.config_path = config_path
        self.events = []
        self.refresh()


    def refresh(self):
        """Reload the configuration to populate the event schedule."""
        try:
            with open(self.config_path) as f:
                config = yaml.load(f)
        except Error:
            config = {}

        now = datetime.now()
        self.events = []

        # Load the scheduled events and drop any that have already happened.
        for e in config['schedule']:
            time = datetime.strptime(e['time'], "%Y-%m-%dT%H:%M:%S")
            label = e['label']
            image = e.get('image', label)
            audio = e.get('audio', label)
            if now < time:
                event = Event(time, label, image, audio, e.get('ad_prefix'))
                self.events.append(event)


    def next_event(self, before=datetime.now()):
        """
        Return the next scheduled event occurring before the given time.
        """
        if not self.events:
            return None
        else:
            event = self.events[0]
            if event.time <= before:
                return event
            else:
                return None


    def advance(self, event_key=None):
        """
        Drop the next scheduled event, optionally checking that it has a
        matching time and label. Returns the dropped event, or None.
        """
        if not self.schedule:
            return None

        first = self.schedule[0]

        if event_key == first.event_key():
            self.schedule.pop(0)
            return first
        else:
            return None
