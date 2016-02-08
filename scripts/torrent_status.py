#!/usr/bin/env python
import transmissionrpc
tc = transmissionrpc.Client('127.0.0.1', port=9091)
current_torrents = tc.get_torrents()
for t in current_torrents:
    print t.name
    print t.sizeWhenDone
    print t.rateUpload
    print t.rateDownload
    print t.leftUntilDone

