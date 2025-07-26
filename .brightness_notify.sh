#!/bin/bash

brightness=$(brightnessctl get)
max_brightness=$(brightnessctl max)
percent=$(( 100 * brightness / max_brightness ))

notify-send -u low -h int:value:$percent -h string:x-canonical-private-synchronous:brightness "Brightness: $percent%" -t 1000

