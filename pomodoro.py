#!/usr/bin/env python
import os
import subprocess
from tqdm import tqdm
from time import sleep
import sys

AUDIO_FILE = 'solemn.mp3'

def notify():
    os.system("osascript -e 'display notification \"Pomodoro session complete!\" with title \"Done!\"'")
    subprocess.call(['afplay', AUDIO_FILE])

def pomodoro(duration):
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
    notify()

def main():
    args = sys.argv
    duration = int(args[1]) if len(args) > 1 else 25
    pomodoro(duration)

if __name__ == '__main__':
    main()
