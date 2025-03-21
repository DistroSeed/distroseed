import os
import sys
sys.path.append("/app/")
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distroseed.settings')
application = get_wsgi_application()

from dashboard.models import AutoTorrent
import requests
import transmissionrpc
from bs4 import BeautifulSoup
from django.conf import settings
from urllib.parse import urljoin

current_autotorrents = AutoTorrent.objects.all()
for torrent_obj in current_autotorrents:
    link = torrent_obj.url
    exclude_list = torrent_obj.excludes.all().values_list('phrase', flat=True)
    include_list = torrent_obj.includes.all().values_list('phrase', flat=True)
    response = requests.get(link, verify=False, timeout=30)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [tag.get("href").strip() for tag in soup.find_all(href=True)]
    sources = [tag.get("src").strip() for tag in soup.find_all(src=True)]
    all_links = links + sources
    links = filter(lambda x:x.strip().endswith(".torrent") or x.strip().startswith("magnet"), all_links)
    torrent_links = [urljoin(link,l) if 'http' not in l else l for l in links]
    torrent_links = [l for l in torrent_links if not any(ex.lower() in l.lower() for ex in exclude_list)]
    tmp_torrent_links = []
    for torrent_link in torrent_links:
        for include_phrase in include_list:
            if include_phrase.lower() in torrent_link.lower():
                tmp_torrent_links.append(torrent_link)
    if tmp_torrent_links:
        torrent_links = tmp_torrent_links
    if torrent_links:
        tc = transmissionrpc.Client(
            settings.TRANSMISSION_HOST,
            port=settings.TRANSMISSION_PORT,
            user=settings.TRANSMISSION_USER,
            password=settings.TRANSMISSION_PASSWORD
        )
        for torrent in torrent_links:
            print(torrent)
            _ = tc.add_torrent(torrent)