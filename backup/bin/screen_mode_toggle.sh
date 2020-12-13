#!/bin/bash

xrandrData=$(xrandr)

t1=$(mktemp /tmp/screen_mode_toggle_t1.XXXXXX)
echo "$xrandrData" | grep "\bconnected\b" > "$t1"

noOfConnectedMon=$(wc -l < "$t1")
rm "$t1"

if [ "$noOfConnectedMon" = "1" ]
then
	echo "Only 1 monitor connected"
	xrandr --output LVDS1 --primary --auto
	exit 0
fi

t2=$(mktemp /tmp/screen_mode_toggle_t2.XXXXXX)
echo "$xrandrData" | grep "\*" > "$t2"

noOfActiveMon=$(wc -l < "$t2")
rm "$t2"



if [ "$noOfActiveMon" = "1" ]
then
	xrandr --output HDMI1 --auto --primary --output LVDS1 --auto --left-of HDMI1
else
	xrandr --output HDMI1 --auto --primary --output LVDS1 --off
fi

exitcode=$?

exit $exitcode
