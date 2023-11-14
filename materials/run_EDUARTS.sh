#!/bin/sh
run_update_file_watcher.sh &
udiskie & 
cd /home/eduarts/geany_code/EDB21NTA1
export DISPLAY=:0
lxterminal --command "python3 main.py" &
