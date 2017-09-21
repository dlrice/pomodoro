#!/usr/bin/env python
import os
import subprocess
from tqdm import tqdm
from time import sleep

AUDIO_FILE = 'solemn.mp3'
DURATION = 25

def notify():
    os.system("osascript -e 'display notification \"Pomodoro session complete!\" with title \"Done!\"'")
    subprocess.call(['afplay', AUDIO_FILE])

def main():
    for i in tqdm(range(DURATION), leave=True, bar_format='{bar} {total} minutes'):
        sleep(60)
    notify()

if __name__ == '__main__':
    main()