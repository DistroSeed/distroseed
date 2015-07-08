#!/usr/bin/env python

from distroseed import scraptorrentlink

url = "http://distrowatch.com/index.php?distribution=all&release=all&month=all&year=2015"
success,failures,blacklist = scraptorrentlink(url)
print success
print failures
print blacklist
