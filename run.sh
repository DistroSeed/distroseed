#!/bin/bash
docker run -d -it --env-file .env -v ./distroseed/db:/app/distroseed/db -v ./torrents/downloads:/data/torrents/downloads -v ./torrents/incomplete:/data/torrents/incomplete -v ./torrents/torrents:/data/torrents/torrents -p8000:8000 -p9091:9091 -p51413:51413 -p51413:51413/udp --name distroseed-$(date -u +"%Y-%m-%d") distroseed bash
docker ps -a