#!/usr/bin/env python
import os
import subprocess
from tqdm import tqdm
from time import sleep
from math import log10
import sys
import signal
from colorama import init
from colorama import Fore
init()

POMODORO_FILE = 'solemn.mp3'
RELAX_FILE = 'to-the-point.mp3'


class Timer(object):
    def __init__(self, duration, start_message, color, notify_message, sound_file):
        self._notify_message = notify_message
        self._sound_file = sound_file
        self._start_message = start_message
        self._progress = 0
        self._color = color
        signal.signal(signal.SIGINT, self.signal_handler)
        self.start(duration)

    def signal_handler(self, signal, frame):
        t = self._progress/60
        print('\nCancelled after {} minutes'.format(t), end='')
        sys.exit(0)

    def notify(self):
        os.system(
            f"osascript -e 'display notification \
            \"{self._notify_message}\" with title \"Done!\"'")
        subprocess.call(['afplay', self._sound_file])

    def start(self, duration):
        t = '{} min '.format(duration)
        args = {
            'leave': True,
            'bar_format': self._color + self._start_message + ' |{bar}| ' + t,
            'ncols': 50 + int(log10(duration))
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
    Timer(duration=1,
          start_message='Rest    ',
          color=Fore.BLUE,
          notify_message='Rest complete',
          sound_file=RELAX_FILE)
    Timer(duration=duration,
          start_message='Pomodoro',
          color=Fore.GREEN,
          notify_message='Pomodoro complete',
          sound_file=POMODORO_FILE)


if __name__ == '__main__':
    main()
