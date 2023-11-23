#!/bin/sh

cp /home/eduarts/swupdate_binary/show /home/eduarts/
chmod 777 /home/eduarts/show
runuser -l eduarts -c /home/eduarts/show &
sleep 2
date=$(date '+%Y-%m-%d-%H-%M-%S')
cd /home/eduarts/
mkdir -p edb_update_history/
tar -czf /home/eduarts/edb_update_history/geany_code_$date.tar.gz geany_code/
rm -rf /home/eduarts/geany_code/*
rm -rf /home/eduarts/geany_code/.*
sync
. /home/eduarts/swupdate_binary/update.sh

sync
sync
sync

reboot
