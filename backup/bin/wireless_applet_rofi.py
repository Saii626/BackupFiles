#!/usr/bin/env python3

import os, re
from subprocess import Popen, run, PIPE
from utils import run_rofi, notify

iwctl = run(['iwctl'], stdin=PIPE, capture_output=True, check=True)
