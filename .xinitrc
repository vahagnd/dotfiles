export XCURSOR_SIZE=12

(sleep 1 && \
if xrandr | grep -q "HDMI1 connected"; then
  xrandr --output HDMI1 --mode 1920x1080 --pos 0x0 \
         --output eDP1 --mode 1366x768 --pos 1920x696 --primary
else
  xrandr --output eDP1 --mode 1366x768 --pos 0x0 --primary
fi) &


exec qtile start

