import subprocess
import copy
import os

WAV_ARGS = ["aplay"]
MP3_ARGS = ["mpg123"]


class AudioController:
    def __init__(self, sound_path):
        self._process = None
        self.sound_path = sound_path

    def kill(self):
        if self._process:
            self._process.kill()
            self._process = None

    def play(self, filename):
        self.kill()

        if filename.lower().endswith(".wav"):
            args = copy.copy(WAV_ARGS)
        elif filename.lower().endswith(".mp3"):
            args = copy.copy(MP3_ARGS)
        else:
            raise Exception("Unknown file extension" + filename)

        args.append(os.path.join(self.sound_path, filename))

        self._process = subprocess.Popen(args)
