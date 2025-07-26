#!/bin/bash

vol=$(amixer get Master | grep -o '[0-9]*%' | head -1)
muted=$(amixer get Master | grep '\[off\]')

if [ -n "$muted" ]; then
  notify-send -u low -h int:value:0 -h string:x-canonical-private-synchronous:volume "Volume Muted" -t 1000
else
  notify-send -u low -h int:value:${vol%\%} -h string:x-canonical-private-synchronous:volume "Volume: $vol" -t 1000
fi

