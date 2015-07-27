#!/bin/bash
current_dir=`pwd`

# rsync all torrent files and exclude everything else

# CentOS
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://rsync.gtlib.gatech.edu/centos/ ${current_dir}/tmp/

# Ubuntu
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://rsync.gtlib.gatech.edu/ubuntu-releases/ ${current_dir}/tmp/

# OpenSUSE
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://rsync.gtlib.gatech.edu/opensuse/distribution/ ${current_dir}/tmp/

# Debian
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://rsync.gtlib.gatech.edu/debian-cd/ ${current_dir}/tmp/

# Arch Linux
rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' rsync://mirrors.kernel.org/archlinux/iso/ ${current_dir}/tmp/

# move torrent files to base dir
find ${current_dir}/tmp/ -regex ".*\.torrent" -exec cp '{}' ${current_dir}/torrents/ \;


# Scrape Links

# Linux Mint
# scrap rss for torrent links
# http://torrents.linuxmint.com/rss/rss.xml

# Fedora
# scrap rss for torrent links
# https://torrent.fedoraproject.org/rss20.xml

# Slackware
# http://www.slackware.com/getslack/torrents.php

# FreeBSD
# not official link but should work
# http://www.gotbsd.net/


# GTG

# Arch Linux
# https://www.archlinux.org/releng/releases/

# Debian
# https://www.debian.org/CD/torrent-cd/

# Ubuntu, etc
# http://torrent.ubuntu.com:6969/

# OpenSUSE
# http://download.opensuse.org/distribution/

# Centos
# http://www.gtlib.gatech.edu/pub/centos/


