#!/bin/bash

PATH=$PATH:~/.local/bin

picom --config /home/saii/.config/picom/conf &
dunst &
sxhkd &
numlockx on

# custom scripts
set_wallpaper.sh  # wallpaper
dbus_script.sh    # store dbus env variable
