#!/usr/bin/env python3

import os
from subprocess import run, Popen, PIPE
from typing import Union, Callable, TypeVar
from enum import Enum

T = TypeVar('T')

def run_rofi(options: [T], prompt: str, converter: Callable[[T], str] = None, preserveInput : bool = False) -> Union[T, str]:
    """
    Runs an arbitary rofi command with specified prompt and options. Then returns the selected
    object. If user didn't select anything, returns None. A converter maybe provided to 
    extract the option to show from provided option. If preserveInput is true, and none of the
    options match user input, returns whatever user entered insread of None
    """

    if converter is None:
        converter = lambda a : a

    optionsMap = { converter(x) : x for x in options }

    rofi = Popen(["rofi", "-i", "-dmenu", "-config", os.path.join(os.getenv('HOME'), 
                    '.config/rofi/applet.rasi') , "-p", prompt + ": "], stdout=PIPE, stdin=PIPE)
    (out, err) = rofi.communicate("\n".join(optionsMap.keys()).encode("utf-8"))

    try:
        retcode = rofi.wait(5)
    except TimeoutExpired:
        rofi.terminate()
        retcode = -1

    if retcode == 0:
        decoded_out = out.decode("utf-8").strip()
        return optionsMap.get(decoded_out, decoded_out if preserveInput else None)

    return None


class Urgency(Enum):
    LOW="low"
    NORMAL="normal"
    CRIT="critical"

def notify(title: str, body: str, urgency: Urgency = Urgency.NORMAL):
    """
    Sends notification. Works even if there is no DBUS_SESSION_BUS_ADDRESS in environment
    """

    if not hasattr(notify, 'env'):
        if 'DBUS_SESSION_BUS_ADDRESS' not in os.environ:
            dbus_file = os.path.join(Path.home(), '.dbus/Xdbus') 
            with open(dbus_file) as f:
                file_contents = f.readline()

            parts = file_contents.split('=', maxsplit=1)

            notify.env = {**os.environ, parts[0].strip(): parts[1].strip()}
        else:
            notify.env = os.environ

    run(['notify-send', '--urgency=%s'%urgency.value, title, body], check=True, env=notify.env)
