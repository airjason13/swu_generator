#!/bin/sh
touch /home/eduarts/run_xxxx
cd /home/eduarts/geany_code/EDB21NTA0
export DISPLAY=:0
pkill -f main.py
sleep 2

lxterminal --command "python3 main.py" &
