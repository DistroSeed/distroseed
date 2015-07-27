#!/usr/bin/python
import os
import requests
import BeautifulSoup
from urlparse import urlparse

tmp_dir='/data/n1/scripts/distroseed/DistroSeed-Dashboard/scripts/tmp/'
final_dir='/data/n1/scripts/distroseed/DistroSeed-Dashboard/scripts/torrents/'

rsync_list = [
    'rsync://rsync.gtlib.gatech.edu/centos/',
    'rsync://rsync.gtlib.gatech.edu/ubuntu-releases/',
    'rsync://rsync.gtlib.gatech.edu/opensuse/distribution/',
    'rsync://rsync.gtlib.gatech.edu/debian-cd/',
    'rsync://mirrors.kernel.org/archlinux/iso/',    
]

strip_links = [
    'http://www.slackware.com/getslack/torrents.php',
    'http://www.gotbsd.net/',
]

rss_pull = [
    'http://torrents.linuxmint.com/rss/rss.xml',
    'https://torrent.fedoraproject.org/rss20.xml',
]


def stripper(url):
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    pagelinks = []
    downloadlinks = []
    response = requests.get(url)
    page = str(BeautifulSoup.BeautifulSoup(response.content))
    start_link = page.find("a href")

    def getURL(page):
	start_link = page.find("a href")
	if start_link == -1:
		return None, 0
	start_quote = page.find('"', start_link)
	end_quote = page.find('"', start_quote + 1)
	url = page[start_quote + 1: end_quote]
	return url, end_quote

    while True:
	url, n = getURL(page)
	page = page[n:]
	if url:
		pagelinks.append(url)
	else:
		break

    # filter down to only links that endwith .torrent
    # TODO: might exclude links that have variables at the end
    links = filter(lambda x:x.endswith(".torrent"), pagelinks)
    links.append(filter(lambda x:x.endswith("/torrent/"), pagelinks))
    links = [x for x in links if x != []]

    fixedlinks = [ domain + str(x) for x in links if 'http' not in x ]
    correctlinks = [ x for x in links if 'http' in x ]
    links = fixedlinks + correctlinks
    for link in links:
        os.system('wget -q --directory-prefix="%s" %s >/dev/null' % (final_dir,link))



for link in strip_links:
    stripper(link)
