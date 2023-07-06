#!/bin/sh
pipewire &
feh --bg-scale $XDG_PICTURES_DIR/wallpapers/2D7478E3-402D-4C8B-AB1C-032F461A9BB5.jpg &
pipewire-pulse &
picom --config $HOME/.config/picom.conf &
wireplumber &
pa-applet &
nm-applet &
lxpolkit &
kdeconnectd &
kdeconnect-indicator &
dunst &
# End of file
