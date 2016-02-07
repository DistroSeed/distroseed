#!/usr/bin/env python
import re
import requests

link_list = [
    # xubuntu
    "http://xubuntu.org/getxubuntu/",
    # kali
    "https://www.kali.org/downloads/",
    # archlinux
    "http://mirror.rackspace.com/archlinux/iso/latest/",
    # ubuntu
    "http://www.ubuntu.com/download/alternative-downloads",
    # debian
    "http://cdimage.debian.org/cdimage/release/current/amd64/bt-dvd/",
    # opensuse
    "http://www.gtlib.gatech.edu/pub/opensuse/distribution/openSUSE-stable/iso/",
    # centos
    "https://mirrors.kernel.org/centos/7/isos/x86_64/",
    # raspbian
    "https://www.raspberrypi.org/downloads/raspbian/",
    # fedora
    "https://torrent.fedoraproject.org/torrents/",    
    # slackware
    "http://www.slackware.com/torrents/",    
]

exclude_list = [
   "-livegnome",
   "-update",
   "-livekde",
   "-light",
   "-mini",
   "-source",
]

for link in link_list:
    r = requests.get(link) 
    data = [x[1] for x in re.findall('(src|href)="(\S+)"',r.content)]
    links = filter(lambda x:x.endswith(".torrent"), data)
    torrent_links = [link + l if 'http' not in l else l for l in links]
    if 'fedora' in link:
        torrent_links = [l for l in torrent_links if 'alpha' not in l.lower() and 'beta' not in l.lower()]    
        torrent_links = [l for l in torrent_links if 'server' in l.lower()]    
    # global exclude 
    torrent_links = [l for l in torrent_links if not any(ex.lower() in l.lower() for ex in exclude_list)]
    print torrent_links
