#!/usr/bin/env python

import os
import re
import requests
import subprocess
import BeautifulSoup

def scraptorrentlink(url):
    # example usage
    # url = "http://distrowatch.com/index.php?distribution=all&release=all&month=all&year=2015"
    # success,fails = scraptorrentlink(url)

    pagelinks = []
    template_dicts = []
    current_torrents = []
    downloadlist = []
    blacklist = []
    successful = []

    with open(os.getcwd() + '/blacklist.txt') as f:
        blacklist = f.read().splitlines()

    cmd = 'transmission-remote -l'
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    text_table = p.stdout.read()

    row_splitter = re.compile("  +")
    rows = text_table.split('\n')
    headings_row = rows[0]
    headings = row_splitter.split(headings_row)
    sum_row = rows[-2]
    rows.pop(0)
    rows.pop()
    rows.pop()

    for row in rows:
        values = row_splitter.split(row)
        template_dict = dict(zip(headings, values))
        template_dicts.append(template_dict)

    for dic in template_dicts:
        current_torrents.append(re.sub('.iso$', '', dic['Name'].lower()))

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

    # make sure we don't already have the torrent
    for url in links:
        file_name = re.sub('.torrent$', '', url.split('/')[-1]).lower()
        file_name = re.sub('.iso$', '', file_name)
        if file_name not in current_torrents and url not in blacklist:
            downloadlist.append(url)

    for link in downloadlist:
        command = subprocess.call(["transmission-remote", "--add", link, "--stop"], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        if command == 0:
            # print "Added %s to Transmission ..." % link
            successful.append(link)
        else:
            blacklist.append(link)
            # print "Failed %s ... blacklisting" % link
    # writing blacklist to file
    with open(os.getcwd() + '/blacklist.txt', 'w') as f:
        f.write('\n'.join(blacklist))
    return successful,blacklist


