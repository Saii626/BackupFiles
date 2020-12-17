#!/usr/bin/env python3

from __future__ import print_function
import os, subprocess, sys
from pathlib import Path
from enum import Enum

class Urgency(str, Enum):
	LOW = 'low'
	MEDIUM = 'normal'
	HIGH = 'critical'

def notify(urgency: Urgency, title: str, body: str):
        """
        Helper function to easily call notify-send
        """
        subprocess.run(['notify-send', '--app-name=app.saikat.SyncConfigurations',
                '--urgency=%s'%urgency.value, title, body], check=True, env=notify.env)

# Use DBUS_SESSION_BUS_ADDRESS so that we can show notification even if run
# from SHELL which don't have the env variable (eg: cronjob)
if 'DBUS_SESSION_BUS_ADDRESS' not in os.environ:
        dbus_file = os.path.join(Path.home(), '.dbus/Xdbus') 
        with open(dbus_file) as f:
                file_contents = f.readline()

        parts = file_contents.split('=', maxsplit=1)

        notify.env = {**os.environ, parts[0].strip(): parts[1].strip()}
else:
        notify.env = os.environ

PROJECT_DIR = Path(__file__).resolve().parent

WORKING_DIR = Path.cwd()

BACKUP_DIR = Path(PROJECT_DIR).joinpath('backup')

if not BACKUP_DIR.exists():
        log.info('backup folder doesnot exists. Creating one')
        BACKUP_DIR.mkdir()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
