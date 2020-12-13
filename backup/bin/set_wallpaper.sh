#! /bin/bash

if [ $# -eq 1 ]
then
	cp -f $1 ~/Pictures/walpaper
fi

feh --bg-scale ~/Pictures/walpaper
