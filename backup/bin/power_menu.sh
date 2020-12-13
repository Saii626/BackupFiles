#!/bin/bash


options=" logout
  sleep
  hibernate
  reboot
  shutdown"


selection=$(echo -e "${options}" | rofi -dmenu -config ~/.config/rofi/power_menu.rasi -p "")

if [ "$?" -eq "1" ]
then
	echo "No selection"
	exit 0
fi

echo "This is your selection: \"$selection\""

case "${selection}" in
    " logout")
	session=$(loginctl session-status | awk 'NR==1{print $1}')
	loginctl terminate-session $session
        echo "Logging out"
        i3-msg exit;;
    "  sleep")
        echo "Suspending system"
        systemctl suspend;;
    "  hibernate")
        echo "Hibernating system"
        systemctl hibernate;;
    "  reboot")
        echo "Rebooting"
        systemctl reboot;;
    "  shutdown")
        echo "Shutting down"
        systemctl poweroff -i;;
esac
