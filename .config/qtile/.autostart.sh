#!/bin/sh

sleep 1.1

# wallpaper
feh --no-fehbg --bg-scale '/home/vahagnd/.config/qtile/pics/max768.jpg' '/home/vahagnd/.config/qtile/pics/max1080.jpg' &

# compositor
picom --config ~/.config/picom/picom.conf &

# notification daemon
dunst &

# numlock
numlockx on &

# Set keyboard layout: US, Russian (phonetic winkeys), Armenian (phonetic)
setxkbmap -layout "us,ru,am" -variant ",phonetic_winkeys,phonetic" -option "grp:win_space_toggle" &

