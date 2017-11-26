#!/usr/bin/env python
import os
import subprocess
from tqdm import tqdm
from time import sleep
import sys
import signal

AUDIO_FILE = 'solemn.mp3'


class Pomodoro(object):

    def __init__(self, duration):
        self._progress = 0
        signal.signal(signal.SIGINT, self.signal_handler)
        self.start(duration)

    def signal_handler(self, signal, frame):
        t = self._progress/60
        print('\nCancelled after {} minutes'.format(t), end='')
        sys.exit(0)


    def notify(self):
        os.system("osascript -e 'display notification \"Pomodoro session complete!\" with title \"Done!\"'")
        subprocess.call(['afplay', AUDIO_FILE])

    def start(self, duration):
        s = '{} min '.format(duration)
        args = {
            'leave': True,
            'bar_format': '|{bar}| ' + s,
            'ncols': max(duration*2, 50)
        }
        niterations = 25
        sleep_duration = 60 * duration / niterations
        for i in tqdm(range(niterations), **args):
            sleep(sleep_duration)
            self._progress = (i + 1) * sleep_duration
        self.notify()


def main():
    args = sys.argv
    duration = int(args[1]) if len(args) > 1 else 25
    Pomodoro(duration)


if __name__ == '__main__':
    main()
