#!/bin/sh
sudo rfkill unblock wifi
run_update_file_watcher.sh &
udiskie &
connect_ovpn_server.sh &
sleep 10
edb_check

cd /home/eduarts/geany_code/EDB21NTA0
export DISPLAY=:0
sleep 2
xrandr > /home/eduarts/xrandr_info_1
xrandr --output HDMI-2 --primary --left-of HDMI-1
sleep 2
xrandr > /home/eduarts/xrandr_info_2
lxterminal --command "python3 main.py" &
