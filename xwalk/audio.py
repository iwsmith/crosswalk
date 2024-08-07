import logging
import os
import subprocess


WAV_COMMAND = ["/usr/bin/aplay"]
MP3_COMMAND = ["/usr/bin/mpg123"]

logger = logging.getLogger(__name__)


class AudioController:
    """
    Controller to play audio files.
    """

    def __init__(self):
        """Construct a new audio controller."""
        self._process = None
        self._playing = None


    def _play_command(self, path):
        """Return a list of command line arguments for playing the sound."""
        args = []
        if path.lower().endswith(".wav"):
            args.extend(WAV_COMMAND)
        elif path.lower().endswith(".mp3"):
            args.extend(MP3_COMMAND)
        else:
            raise Exception("Unknown file extension" + path)
        args.append(path)
        return args


    def playing(self):
        """Return a vector of information about the currently playing animations."""
        return [path for path in self._playing or []]


    def kill(self):
        """Kill the currently playing sound, if any."""
        if self._process:
            #logger.debug("Killing: %s", self._playing)
            subprocess.call(['/usr/bin/pkill', '-P', str(self._process.pid)])
            self._process.kill()
            self._process = None
        self._playing = None


    def play(self, animation):
        """Play a sound file. Any currently playing sound will be replaced."""
        self.kill()

        path = animation and animation.audio_path
        if path is None:
            return

        command = self._play_command(path)
        logger.info("Playing: %s", path)

        self._process = subprocess.Popen(command)
        self._playing = [path]


    def play_all(self, animations):
        """
        Play the given audio files in sequence. Any currently playing audio
        will be replaced.
        """
        self.kill()

        paths = [
            animation.audio_path
            for animation in animations
            if animation and animation.audio_path
        ]

        if not paths:
            return

        commands = [" ".join(self._play_command(path)) for path in paths]
        script = " && ".join(commands)
        logger.info("Playing all: %s", paths)

        self._process = subprocess.Popen(script, shell=True)
        self._playing = paths
