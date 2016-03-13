#!/bin/bash
yum install -y epel-release
yum install -y httpd tranmission-cli transmission-daemon transmission python-pip git nano mod_wsgi python-requests python-BeautifulSoup policycoreutils-python
echo '127.0.0.1 distroseed' >> /etc/hosts
pip install --upgrade pip
pip install django
pip install transmissionrpc
pip install hurry.filesize
mkdir /data
mkdir /data/downloads
mkdir /data/downloads/complete
mkdir /data/downloads/incomplete
mkdir /data/downloads/torrents
cd /data
git clone https://github.com/DistroSeed/distroseed.git
rm -f /etc/httpd/conf.d/*
cp -f /data/distroseed/conf/distroseed.conf /etc/httpd/conf.d/distroseed.conf
cp -f /data/distroseed/conf/50-allow-apache-systemd.pkla /etc/polkit-1/localauthority/50-local.d/50-allow-apache-systemd.pkla
cp -f /data/distroseed/conf/settings.json /var/lib/transmission/.config/transmission-daemon/settings.json
cp -f /data/distroseed/conf/transmission-daemon.service /usr/lib/systemd/system/transmission-daemon.service
cd /data/distroseed/conf
semodule -i /data/distroseed/conf/allow_httpd_dbus_dir.pp
semodule -i /data/distroseed/conf/allow_httpd_systemctl_execute_no_trans.pp
semodule -i /data/distroseed/conf/allow_httpd_systemctl_policykit.pp
semodule -i /data/distroseed/conf/allow_httpd_systemctl.pp
semodule -i /data/distroseed/conf/allow_httpd_systemctl_read.pp
semodule -i /data/distroseed/conf/allow_httpd_systemctl_start.pp
semodule -i /data/distroseed/conf/allow_httpd_write_var.pp
setsebool -P httpd_can_network_connect on
chmod 660 /var/lib/transmission/.config/transmission-daemon/settings.json
chown -R apache:apache /data
chcon -R -t httpd_sys_content_rw_t /data
chown -R transmission:transmission /data/downloads
systemctl daemon-reload
systemctl start httpd
systemctl enable httpd
systemctl enable firewalld
systemctl start firewalld
firewall-cmd --zone=public --add-port=80/tcp --permanent
firewall-cmd --reload
systemctl start transmission-daemon
systemctl enable transmission-daemon
systemctl start transmission-daemon
systemctl stop transmission-daemon
