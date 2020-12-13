#!/bin/bash

noOfMonOld=-1
while true
do
	xrandrData=$(xrandr)

	t1=$(mktemp /tmp/screen_mode_state_t1.XXXXXX)
	echo "$xrandrData" | grep "\bconnected\b" > "$t1"

	noOfMon=$(wc -l < "$t1")
	rm "$t1"

	if [ "$noOfMonOld" = "-1" ]
	then
		echo "Executing for the first time"
		noOfMonOld="$noOfMon"

		t2=$(mktemp /tmp/screen_mode_state_t2.XXXXXX)
		echo "$xrandrData" | grep "\*" > "$t2"

		noOfActiveMon=$(wc -l < "$t2")
		rm "$t2"

		if [ "$noOfActiveMon" = "2" ]
		then
			screen_mode_toggle.sh
		fi
		continue
	fi	

	if [ "$noOfMon" != "$noOfMonOld" ]
	then
		echo "No of connected monitors changed from $noOfMonOld to $noOfMon"
		screen_mode_toggle.sh
	fi
	noOfMonOld="$noOfMon"

	sleep 5
done


