#! /usr/bin/env bash

sudo pacman -S openssh git --needed base-devel

# 
# Make a Projects folder in home and start pulling repos
#

cd ~
mkdir Projects
cd Projects

# Make aur helper 'paru'
git clone https://aur.archlinux.org/paru.git
cd paru
makepkg -si
cd ..

# CSS themes. Used by qutebrowser
https://github.com/alphapapa/solarized-everything-css

# My patched version of st
https://github.com/Saii626/st
cd st
make
sudo make install
cd ..

# restore backed up locations
git clone https://github.com/Saii626/BackupFiles
cd BackupFiles
sudo chmod +x backup.py
./backup.py restore

# Install applications
pacman=(
	aria2c
	calibre
	chromium-widevine
	clang
	cmake
	code
	dunst
	evince
	fcron
	fd
	feh
	ffmpegthumbnailer
	firefox
	gnu-netcat
	gradle
	grub
	htop
	i3-wm
	i3blocks
	iw
	iwd
	lastpass-cli
	lightdm
	lightdm-gtk-greeter
	lightdm-webkit-theme-litarvan
	man-db
	man-pages
	ncpamixer
	neovim
	net-tools
	nmap
	numlockx
	openjdk-doc
	openjd-src
	otf-fira-mono
	picom
	plocate
	pulseaudio
	pulseaudio-alsa
	python-pymupdf
	python-pyperclip
	qutebrowser
	ranger
	redshift
	reflector
	rofi-calc
	screen
	sshfs
	sudo
	sxhkd
	termite
	ttf-fira-code
	ttf-fira-mono
	ttf-nerd-fonts-symbols
	udiskie
	ueberzug
	unclutter
	vlc
	wget
	wireless_tools
	xclip
	xf86-video-amdgpu
	xorg-server
	xorg-xinit
	xorg-xinput
	zathura
	zathura-djvu
	zathura-pdf-mupdf
	zip
	zsh
	zsh-syntax-highlighting
	)
paru=(
	nnn-nerd
	minecraft-launcher
)

sudo pacman -Syu ${pacman[@]}
paru -S ${paru[@]}
