#!/bin/bash
current_dir=`pwd`
# rsync all torrent files and exclude everything else
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://ftp.gtlib.gatech.edu/ ${pwd}/tmp/
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://mirrors.kernel.org/mirrors/ ${pwd}/tmp/
# move those torrent files back to the root directory of the folder
find ${pwd}/tmp/ -regex ".*\.torrent" -exec cp '{}' ${pwd}/torrents/ \;



######
# Linux Mint
# scrap rss for torrent links
# http://torrents.linuxmint.com/rss/rss.xml

# Ubuntu, etc
# scrap all links since they are the torrent files
# http://torrent.ubuntu.com:6969/

# Debian
# scrap for links to torrent links
# https://www.debian.org/CD/torrent-cd/

# Fedora
# scrap rss for torrent links
# https://torrent.fedoraproject.org/rss20.xml

# OpenSUSE
# recrusively look through each folder for torrent files
# http://download.opensuse.org/distribution/

# Arch Linux
# scrap links for /torrent/
# https://www.archlinux.org/releng/releases/

# Centos
# recursively search for torrent links; still better with rsync
# http://www.gtlib.gatech.edu/pub/centos/

# Slackware
# http://www.slackware.com/getslack/torrents.php

# FreeBSD
# not official link but should work
# http://www.gotbsd.net/
