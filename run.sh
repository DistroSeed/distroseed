#!/bin/bash
docker run -d -it --env-file .env -v ./distroseed/db:/app/distroseed/db -v ./torrents/downloads:/data/torrents/downloads -v ./torrents/torrents:/etc/transmission-daemon/torrents -p8000:8000 -p9091:9091 -p51414:51414 -p51414:51414/udp --name distroseed-$(date -u +"%Y-%m-%d") distroseed bash
docker ps -a