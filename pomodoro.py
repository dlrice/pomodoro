#!/usr/bin/env python
import os
import subprocess
from tqdm import tqdm
from time import sleep
from math import log10, trunc
import sys
import signal
import datetime
from colorama import init
from colorama import Fore
init()

POMODORO_FILE = 'solemn.mp3'
RELAX_FILE = 'to-the-point.mp3'

sys.tracebacklimit = 0

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
        m, s = divmod(self._progress, 60)
        m = trunc(m)
        s = trunc(s)
        print(Fore.CYAN + f'\nCancelled after {m:d} minutes and {s:d} seconds', end='')
        sys.exit(0)

    def notify(self):
        os.system(
            f"osascript -e 'display notification \"{self._notify_message}\" with title \"Done!\"'")
        subprocess.call(['afplay', self._sound_file])

    def start(self, duration):
        t = f'{duration} min '
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

    now = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
    print(Fore.CYAN + f'Started at {now}')

    Timer(duration=1,
          start_message='Prepare ',
          color=Fore.BLUE,
          notify_message='Preparation complete',
          sound_file=RELAX_FILE)
    Timer(duration=duration,
          start_message='Pomodoro',
          color=Fore.GREEN,
          notify_message='Pomodoro complete',
          sound_file=POMODORO_FILE)


if __name__ == '__main__':
    main()
