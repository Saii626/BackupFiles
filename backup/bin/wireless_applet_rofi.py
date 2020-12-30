#!/usr/bin/env python3

import os, re, sys, time
from subprocess import Popen, run, PIPE
from utils import run_rofi, notify

iwctl = Popen(['iwctl'], stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding='utf-8')

iwctl.stdin.write('station wlan0 show')
time.sleep(1)
print('Err: "%s"'%iwctl.stderr.read(2))
print('Out: "%s"'%iwctl.stdout.read(100))


cmd = input("Cmd:")
outs, errs = iwctl.stdin.write(cmd)
print('Err: "%s"'%errs.decode('utf-8'))
print('Out: "%s"'%outs.decode('utf-8'))
