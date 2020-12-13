#!/bin/bash

if [ $# -eq 0 ]
then
	echo "No theme specified"
	exit 1
fi

theme=$1

cd ~/.base16

# Inject basic color schemes
pybase16 inject -s "$theme" -f ~/.config/i3/config -f ~/.config/dunst/dunstrc \
			-f ~/.config/i3status/config -f ~/.config/rofi/config.rasi \
			-f ~/.config/rofi/power_menu.rasi -f ~/.config/rofi/ask_pass.rasi \
			-f ~/.config/rofi/applet.rasi -f ~/.config/termite/config \
			-f ~/.config/polybar/config -f ~/.config/qutebrowser/config.py \
			-f ~/.Xresources


# Set colorscheme of nvim
sed -E -i "s/colorscheme.*/colorscheme base16-$theme/" ~/.config/nvim/init.vim

# reload Xresources
xrdb ~/.Xresources

# Configure transparancies
sed -E -i "s/background:(.*), 100 %/background:\1, 90 %/" ~/.config/rofi/config.rasi
sed -E -i "s/background:(.*), 100 %/background:\1, 90 %/" ~/.config/rofi/power_menu.rasi
sed -E -i "s/background:(.*), 100 %/background:\1, 90 %/" ~/.config/rofi/ask_pass.rasi
sed -E -i "s/background:(.*), 100 %/background:\1, 90 %/" ~/.config/rofi/applet.rasi

hexcolor=$(sed -E "s/^background.*=.*#(.*)/\\1/;t;d" ~/.config/termite/config)
rgbacol=$(printf "rgba(%d, %d, %d, 0.9)\n" 0x${hexcolor:0:2} 0x${hexcolor:2:2} 0x${hexcolor:4:2})
sed -E -i "s/^background.*=.*#(.*)/background = ${rgbacol}/" ~/.config/termite/config
