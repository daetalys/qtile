#!/usr/bin/env bash

function run {
  if ! pgrep -f $1 ;
  then
    $@&
  fi
}
run pipewire &
run pipewire-pulse &
run wireplumber &
run pa-applet &
run nm-applet &
run polkit-qt5 &
run kdeconnectd &
run kdeconnect-indicator &
run mako &
run protonmail-bridge &
