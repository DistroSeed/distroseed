#!/usr/bin/env python

import os
import re
import time
import requests
import subprocess
import BeautifulSoup
import transmissionrpc

def scraptorrentlink(url,ip='127.0.0.1',port=9091):
    # example usage
    # url = "http://distrowatch.com/index.php?distribution=all&release=all&month=all&year=2015"
    # success,failures,blacklist = scraptorrentlink(url)

    pagelinks = []
    downloadlist = []
    currentlist = []
    blacklist = []
    successful = []
    failures = []

    # Pull blacklist file into blacklist variable
    with open(os.getcwd() + '/blacklist.txt') as f:
        blacklist = f.read().splitlines()

    # Setup transmission connection
    tc = transmissionrpc.Client(ip, port=port)

    # Get list of current torrents in transmission
    current_torrents = tc.get_torrents()

    # Turn torrent objects into a name list
    for tobject in current_torrents:
        currentlist.append(tobject.name)

    # Scrap torrents off link provided
    response = requests.get(url)
    page = str(BeautifulSoup.BeautifulSoup(response.content))
    start_link = page.find("a href")

    def getURL(page):
        start_link = page.find("href")
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
        # strip the link down to the filename
        file_name = re.sub('.torrent$', '', url.split('/')[-1]).lower()
        # strip the .iso extention
        file_name = re.sub('.iso$', '', file_name)
        # see if the file is currently in tranmission or blacklisted
        if file_name not in currentlist and url not in blacklist:
            downloadlist.append(url)

    # looping through the downloadlist to add to transmission
    for link in downloadlist:
        try:
            # add torrent link to transmission
            tc.add_torrent(link)
            # add link to successful list if doesnt fail
            successful.append(link)
        except:
            # if url adding to transmission fails, blacklist it
            blacklist.append(link)
            # add to failures list to return
            failures.append(link)
        # add time delay to keep from crashing transmission
        time.sleep(1)

    # writing blacklist to file
    with open(os.getcwd() + '/blacklist.txt', 'w') as f:
        f.write('\n'.join(blacklist))
    # return lists of what was successful and what failed and whats blacklisted
    return successful,failures,blacklist


def purgeall(ip='127.0.0.1',port=9091,purge_data=False):

    currentlist = []

    # Setup transmission connection
    tc = transmissionrpc.Client(ip, port=port)

    # Get list of current torrents in transmission
    current_torrents = tc.get_torrents()
    
    # Turn torrent objects into a name list
    for tobject in current_torrents:
        currentlist.append(tobject.hashString)

    # See if transmission has any torrents in it
    if len(currentlist)==0 or currentlist is None:
        return True

    # remove all the torrents and their data
    try:
        tc.remove_torrent(currentlist,delete_data=purge_data)
        return True
    except:
        return False

def torrentstatusall(ip='127.0.0.1',port=9091):

    currentlist = []

    # Setup transmission connection
    tc = transmissionrpc.Client(ip, port=port)

    # Get list of current torrents in transmission
    current_torrents = tc.get_torrents()

    # See if transmission has any torrents in it
    if len(current_torrents)==0 or current_torrents is None:
        return current_torrents
    
    # Turn torrent objects into a list of statuses
    for tobject in current_torrents:
        try:
            status = tobject.eta
	except:
            status = None
        currentlist.append({
            'hashstring':tobject.hashString,
            'name':tobject.name,
            'status':tobject.status,
            'eta':status,            
        })

    # return list of torrents and status
    try:
        return currentlist
    except:
        return currentlist

