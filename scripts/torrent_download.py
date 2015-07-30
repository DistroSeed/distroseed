#!/usr/bin/env python

import transmissionrpc
from distroseed import torrentstatusall

ip="10.20.254.20"
port=9091
downloadnow = []
torrent_limit = 0

# Setup transmission connection
tc = transmissionrpc.Client(ip, port=port)

statuses = torrentstatusall()

for status in statuses:
    download_status = status['status']
    if download_status == 'downloading' or download_status == 'download pending':
        torrent_limit = torrent_limit + 1

for status in statuses:
    if torrent_limit == 5:
        break
    else:
        download_status = status['status']
        if download_status == 'downloading' or download_status == 'download pending':
            continue
        if download_status == 'stopped':
            hash = status['hashstring']
            downloadnow.append(hash)
            torrent_limit = torrent_limit + 1
            tc.start(hash)
            continue
        else:
            continue
