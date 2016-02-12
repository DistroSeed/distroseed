# DistroSeed-Dashboard
DistroSeed is an automated assistant for finding, downloading, and managing Linux Distributions through the Transmission torrent application.

### Features Include: ###
* Great looking dashboard and management interface.
* Automated handling of Linux distributions leveraging DistroWatch tracking information.
* Management of bandwidth allocations, storage limiters, and auto pruning of old torrents.
* Feel good for supporting Linux distribution efforts.

### Take a Peak ###
* [At our site](https://distroseed.com)

### Contributions ###
* Co founded by Ian Norden and Leon Denard, primary contributors include Chris Neal and Scott Groveman.

### License ###
* [GNU GPL v3](http://www.gnu.org/licenses/gpl.html)
Copyright 2010-2016


### Setup Guide (incomplete) ###
<code>yum install -y epel-release</code><br />
<code>yum install -y httpd tranmission-cli transmission-daemon transmission python-pip git nano mod_wsgi python-requests python-BeautifulSoup</code><br />
<code>pip install --upgrade pip</code><br />
<code>pip install django</code><br />
<code>pip install transmissionrpc</code><br />
<code>pip install hurry.filesize</code><br />
<code>echo '127.0.0.1   distroseed distroseed.pingnattack.com' >> /etc/hosts</code><br />
<code>mkdir /data</code><br />
<code>rm -f /etc/httpd/conf.d/*</code><br />
<code>nano /etc/httpd/conf.d/distroseed.conf</code><br />
<blockquote>
<pre>
&lt;VirtualHost *:80&gt;
        ServerName distroseed.pingnattack.com
        ServerAlias distroseed
        WSGIScriptAlias / /data/distroseed/distroseed/wsgi.py
        &lt;Directory "/data/distroseed/distroseed/"&gt;
                Order deny,allow
                Allow from all
                Require all granted
        &lt;/Directory&gt;
        Alias /media /data/distroseed/media/
        &lt;Directory "/data/distroseed/media/"&gt;
                Order deny,allow
                Allow from all
                Require all granted
        &lt;/Directory&gt;
        Alias /static /data/distroseed/media/static
        &lt;Directory "/data/distroseed/media/static"&gt;
                Order deny,allow
                Allow from all
                Require all granted
        &lt;/Directory&gt;
&lt;/VirtualHost&gt;
</pre>
</blockquote>
<code>systemctl start httpd</code><br />
<code>systemctl enable httpd</code><br />
<code>firewall-cmd --zone=public --add-port=80/tcp --permanent</code><br />
<code>firewall-cmd --reload</code><br />
<code>systemctl enable firewalld</code><br />
<code>systemctl start firewalld</code><br />
<code>chcon -R -t httpd_sys_content_rw_t /data</code><br />
<code>python manage.py makemigrations</code><br />
<code>python manage.py migrate</code><br />
<code>python manage.py createsuperuser</code><br />
<code>chown -R apache:apache /data</code><br />
<code>systemctl enable transmission-daemon</code><br />
<code>systemctl start transmission-daemon</code><br />
<code>mkdir /data/downloads</code><br />
<code>mkdir /data/downloads/complete</code><br />
<code>mkdir /data/downloads/incomplete</code><br />
<code>mkdir /data/downloads/torrents</code><br />
<code>chown -R transmission:transmission /data/downloads</code><br />
<code>chmod -R g+rwxs /data/downloads/torrents</code><br />
<code>systemctl stop transmission-daemon</code><br />
<code>nano /var/lib/transmission/.config/transmission-daemon/settings.json</code><br />
<blockquote><pre>
{
    "alt-speed-down": 50, 
    "alt-speed-enabled": false, 
    "alt-speed-time-begin": 540, 
    "alt-speed-time-day": 127, 
    "alt-speed-time-enabled": false, 
    "alt-speed-time-end": 1020, 
    "alt-speed-up": 50, 
    "bind-address-ipv4": "0.0.0.0", 
    "bind-address-ipv6": "::", 
    "blocklist-enabled": false, 
    "blocklist-url": "http://www.example.com/blocklist", 
    "cache-size-mb": 10, 
    "dht-enabled": true, 
    "download-dir": "/data/downloads/complete", 
    "download-queue-enabled": true, 
    "download-queue-size": 5, 
    "encryption": 2, 
    "idle-seeding-limit": 30, 
    "idle-seeding-limit-enabled": false, 
    "incomplete-dir": "/data/downloads/incomplete", 
    "incomplete-dir-enabled": true, 
    "lpd-enabled": false, 
    "message-level": 1, 
    "peer-congestion-algorithm": "", 
    "peer-id-ttl-hours": 6, 
    "peer-limit-global": 200, 
    "peer-limit-per-torrent": 50, 
    "peer-port": 51413, 
    "peer-port-random-high": 65535, 
    "peer-port-random-low": 49152, 
    "peer-port-random-on-start": false, 
    "peer-socket-tos": "default", 
    "pex-enabled": true, 
    "port-forwarding-enabled": true, 
    "preallocation": 1, 
    "prefetch-enabled": 1, 
    "queue-stalled-enabled": true, 
    "queue-stalled-minutes": 30, 
    "ratio-limit": 2, 
    "ratio-limit-enabled": false, 
    "rename-partial-files": true, 
    "rpc-authentication-required": false, 
    "rpc-bind-address": "0.0.0.0", 
    "rpc-enabled": true, 
    "rpc-password": "{c1b7e39a73a4f2d9a0d75781a0c09c07fbfb5d527W3bwH1f", 
    "rpc-port": 9091, 
    "rpc-url": "/transmission/", 
    "rpc-username": "", 
    "rpc-whitelist": "127.0.0.1", 
    "rpc-whitelist-enabled": true, 
    "scrape-paused-torrents-enabled": true, 
    "script-torrent-done-enabled": false, 
    "script-torrent-done-filename": "", 
    "seed-queue-enabled": false, 
    "seed-queue-size": 10, 
    "speed-limit-down": 100, 
    "speed-limit-down-enabled": false, 
    "speed-limit-up": 100, 
    "speed-limit-up-enabled": false, 
    "start-added-torrents": true, 
    "trash-original-torrent-files": false, 
    "umask": 18, 
    "upload-slots-per-torrent": 14, 
    "utp-enabled": true, 
    "watch-dir": "/data/downloads/torrents", 
    "watch-dir-enabled": true
}
</pre></blockquote> 
<code>sudo systemctl start transmission-daemon</code><br />
<code>sudo setsebool -P httpd_can_network_connect on</code><br />
