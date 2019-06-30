from datetime import datetime, timedelta
import logging
import os
import yaml

logger = logging.getLogger(__name__)


class Event:
    """
    A scheduled event.
    """

    def __init__(self, label, time, image, audio, ad=None):
        """Construct a new schedule event."""
        self.label = label
        self.time = time
        self.image = image
        self.audio = audio
        self.ad = ad


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
            if now < time:
                event = Event(time, e['label'], e['image'], e['audio'], e.get('ad'))
                self.events.append(event)


    def next_event(self, before=datetime.now()):
        """
        Return the next scheduled event occurring before the given time.
        """
        if not self.schedule:
            return None
        else:
            event = self.schedule[0]
            if event.time <= before:
                return event
            else:
                return None


    def advance(self, time=None, label=None):
        """
        Drop the next scheduled event, optionally checking that it has a
        matching time and label. Returns the dropped event, or None.
        """
        if not self.schedule:
            return None

        first = self.schedule[0]
        if time is not None and time != first.time:
            return None
        elif label is not None and label != first.label:
            return None
        else:
            self.schedule.pop(0)
            return first
