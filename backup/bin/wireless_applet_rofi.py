#!/usr/bin/env python3

import os, re, sys, time, fcntl
from subprocess import Popen, run, PIPE
from utils import run_rofi, notify

def print_stdout_err(outerr):
	txt = outerr.read(1024)
	while txt:
		print(txt)
		txt = outerr.read(1024)

# Open connection with iwctl
iwctl = Popen(['iwctl'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')

# Fix its stdout and stderr to be non blocking
flags = fcntl.fcntl(iwctl.stdout, fcntl.F_GETFL)
fcntl.fcntl(iwctl.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)

flags = fcntl.fcntl(iwctl.stderr, fcntl.F_GETFL)
fcntl.fcntl(iwctl.stderr, fcntl.F_SETFL, flags | os.O_NONBLOCK)

iwctl.stdin.write('station wlan0 show')
time.sleep(0.5)

print('Err:')
print_stdout_err(iwctl.stdout)
print('Out:')
print_stdout_err(iwctl.stderr)



