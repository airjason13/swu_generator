#!/bin/sh

cp /home/eduarts/swupdate_binary/show /home/eduarts/
chmod 777 /home/eduarts/show
runuser -l eduarts -c /home/eduarts/show &
sleep 5
. /home/eduarts/swupdate_binary/update.sh

sync
sync
sync

reboot
