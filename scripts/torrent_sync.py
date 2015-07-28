#!/usr/bin/python
import os
import re
import glob
import time
import json
import requests
import feedparser
import BeautifulSoup
import transmissionrpc
from urlparse import urlparse

feedparser.USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/39.0"
tmp_dir='/data/n1/scripts/distroseed/DistroSeed-Dashboard/scripts/tmp/'
final_dir='/data/n1/scripts/distroseed/DistroSeed-Dashboard/scripts/torrents/'
ip="10.20.254.20"
port=9091

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

def rss_download(url):
    rssfeed = feedparser.parse(url)
    links = []
    for i in range(0,len(rssfeed)):
        links.append(rssfeed['entries'][i].link)
    for link in links:
        os.system('wget -q --directory-prefix="%s" %s >/dev/null' % (final_dir,link))

def rsync_download(url):
    os.system("rsync -Pav --include '+ */' --include '*.torrent' --exclude '- *' %s %s >/dev/null" % (url,tmp_dir))


## Main ##

# clean out current download folder
os.system("rm -f %s*" % final_dir)

# loop through links to strip for torrent links
for link in strip_links:
    stripper(link)
    print "finished %s..." % link

# loop through rss feeds
for link in rss_pull:
    rss_download(link)
    print "finished %s..." % link

# loop through rsync list to pull torrents from mirrors
for link in rsync_list:
    rsync_download(link)
    print "finished %s..." % link

# move all torrent files to final_dir
os.system("find %s -regex \".*\.torrent\" -exec cp '{}' %s \;" % (tmp_dir,final_dir))

# lists
add_list = []
currentlist = []
successful = []
blacklist = []
failures = []

# Setup transmission connection
tc = transmissionrpc.Client(ip, port=port)

# Get list of current torrents in transmission
current_torrents = tc.get_torrents()

# Turn torrent objects into a name list
for tobject in current_torrents:
	currentlist.append(tobject.name)

# pull list of torrent files
file_list = glob.glob(final_dir + "*.torrent")

# make sure we don't already have the torrent
for file in file_list:
    # strip the link down to the filename
    file_name = re.sub('.torrent$', '', file.split('/')[-1]).lower()
    # strip the .iso extention
    file_name = re.sub('.iso$', '', file_name)
    # see if the file is currently in tranmission or blacklisted
    if file_name not in currentlist:
        add_list.append(file)

# looping through the downloadlist to add to transmission
for file in add_list:
    try:
        # add torrent link to transmission
        tc.add_torrent(file,paused=True)
        # add link to successful list if doesnt fail
        successful.append(file)
        print "successfully added %s..." % file
    except:
        # if url adding to transmission fails, blacklist it
        blacklist.append(file)
        # add to failures list to return
        failures.append(file)
        print "failed to add %s..." % file
    # add time delay to keep from crashing transmission
    time.sleep(1)
