import subprocess
import copy
import os
import logging
import yaml

WAV_ARGS = ["/usr/bin/aplay"]
MP3_ARGS = ["/usr/bin/mpg123"]


class AudioController:
    def __init__(self, sound_path, image_mapping):
        self._process = None
        self.sound_path = sound_path
        self.image_sound_mapping = from_yaml(image_mapping)

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

        logging.info(args)

        self._process = subprocess.Popen(args)

    def image(self, imagename):
        try:
            snd = self.image_sound_mapping[imagename]
            if snd:
                self.play(snd)
        except KeyError:
            self.play(self.image_sound_mapping["default"])


def from_yaml(filename):
    with open(filename) as f:
        image_sound_mapping = yaml.load(f)

    return image_sound_mapping
