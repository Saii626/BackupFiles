#!/bin/bash

# Terminate already running bar instances

killall -q polybar 


polybar status_bar >>/tmp/polybar1.log  2>&1 &

