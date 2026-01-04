#!/bin/bash
docker run -d -it --env-file .env -v /data/distroseed/distroseed/db:/app/distroseed/db -v /mnt/isos/:/data/torrents/downloads -v /data/distroseed/torrents/torrents:/etc/transmission-daemon/torrents -p8000:8000 -p9091:9091 -p51414:51414 -p51414:51414/udp --name distroseed distroseed bash
docker ps -a
