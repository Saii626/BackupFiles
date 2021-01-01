#!/usr/bin/env python3

import subprocess
from utils import run_rofi

# get current status
iwctl = subprocess.run(['iwctl', 'station', 'wlan0', 'show'], text=True, capture_output=True)

print('Err: %s \nOut: %s', iwctl.stderr, iwctl.stdout)



