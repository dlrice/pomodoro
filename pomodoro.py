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

DONE_SOUND_FILE = "airplane-ding-sound.mp3"

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
        print(Fore.CYAN + f"\nCancelled after {m:d} minutes and {s:d} seconds", end="")
        sys.exit(0)

    def notify(self):
        os.system(
            f'osascript -e \'display notification "{self._notify_message}" with title "Done!"\''
        )
        subprocess.call(["afplay", self._sound_file])

    def start(self, duration):
        t = f"{duration} min "
        args = {
            "leave": True,
            "bar_format": self._color + self._start_message + " |{bar}| " + t,
            "ncols": 50 + int(log10(duration)),
        }
        niterations = 25
        sleep_duration = 60 * duration / niterations
        for i in tqdm(range(niterations), **args):
            sleep(sleep_duration)
            self._progress = (i + 1) * sleep_duration
        self.notify()


def stage(n, duration, color):
    Timer(
        duration=duration,
        start_message=f"Stage {n}",
        color=color,
        notify_message="Complete",
        sound_file=DONE_SOUND_FILE,
    )


def main():
    args = sys.argv[1:]
    durations = [int(arg) for arg in args]

    now = datetime.datetime.now().strftime("%H:%M %B %d, %Y")
    print(Fore.CYAN + f"Started at {now}")

    colors = [Fore.LIGHTMAGENTA_EX, Fore.CYAN, Fore.GREEN, Fore.RED]
    for i, duration in enumerate(durations):
        stage(i + 1, duration, colors[i % len(colors)])


if __name__ == "__main__":
    main()
