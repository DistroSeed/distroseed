# DistroSeed-Dashboard
DistroSeed is an automated assistant for finding, downloading, and managing Linux Distributions through the Transmission torrent application.

### Major Features Include: ###
* Great looking dashboard and management interface.
* Automated handling of Linux distributions leveraging DistroWatch tracking information.
* Management of bandwidth allocations, storage limiters, and auto pruning of old torrents.
* Feel good for supporting Linux distribution efforts.

### Setup ###
* Not much to see here currently.

### Development ###
* Interface Preview: https://raw.githubusercontent.com/DistroSeed/DistroSeed-Dashboard/master/images/ScreenshotSamples/distroseed%20dash.PNG

### Contributions ###
* Co founded by Ian Norden and Leon Denard, primary contributors include Chris Neal and Scott Groveman.

### License ###
* [GNU GPL v3](http://www.gnu.org/licenses/gpl.html)
Copyright 2010-2016


### Setup Guide (incomplete) ###
<code>yum install -y epel-release</code><br />
<code>yum install -y httpd tranmission-cli transmission-daemon transmission python-pip git nano mod_wsgi</code><br />
<code>pip install --upgrade pip</code><br />
<code>pip install django</code><br />
<code>pip install transmissionrpc</code><br />
<code>echo '127.0.0.1   distroseed distroseed.pingnattack.com' >> /etc/hosts</code><br />
<code>mkdir /data</code><br />
<code>rm -f /etc/httpd/conf.d/*</code><br />
<code>nano /etc/httpd/conf.d/distroseed.conf</code><br />
<blockquote>
<VirtualHost *:80>
        ServerName distroseed.pingnattack.com
        ServerAlias distroseed
        WSGIScriptAlias / /data/distroseed/distroseed/wsgi.py
        <Directory "/data/distroseed/distroseed/">
                Order deny,allow
                Allow from all
                Require all granted
        </Directory>        
        Alias /media /data/distroseed/media/
        <Directory "/data/distroseed/media/">
                Order deny,allow
                Allow from all
                Require all granted
        </Directory>
        Alias /static /data/distroseed/media/static
        <Directory "/data/distroseed/media/static">
                Order deny,allow
                Allow from all
                Require all granted
        </Directory>
</VirtualHost>
</blockquote>
<code>systemctl start httpd</code><br />
<code>systemctl enable httpd</code><br />
<code>firewall-cmd --zone=public --add-port=80/tcp --permanent</code><br />
<code>firewall-cmd --reload</code><br />
<code>systemctl enable firewalld</code><br />
<code>systemctl start firewalld</code><br />
<code>chcon -R -t httpd_sys_content_rw_t /data</code>
