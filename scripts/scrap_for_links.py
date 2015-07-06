#!/usr/bin/env python

from distroseed import scraptorrentlink

url = "http://distrowatch.com/index.php?distribution=all&release=all&month=all&year=2015"
success,fails = scraptorrentlink(url)
print success
print fails
