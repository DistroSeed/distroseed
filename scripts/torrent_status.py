#!/usr/bin/env python

from distroseed import torrentstatusall

statuses = torrentstatusall()
for status in statuses:
    print status
