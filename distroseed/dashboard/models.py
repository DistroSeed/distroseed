from __future__ import unicode_literals
from django.db import models

class Excludes(models.Model):
    phrase = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.phrase}"

    class Meta:
        verbose_name = 'Exclusions'
        verbose_name_plural = 'Exclusions'

class Includes(models.Model):
    phrase = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.phrase}"

    class Meta:
        verbose_name = 'Inclusions'
        verbose_name_plural = 'Inclusions'

class AutoTorrent(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField(max_length=300)
    excludes = models.ManyToManyField(Excludes, blank=True)
    includes = models.ManyToManyField(Includes, blank=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Automatically Torrent'
        verbose_name_plural = 'Automatically Torrent'

class TransmissionSetting(models.Model):
    alt_speed_down = models.IntegerField(blank=True)
    alt_speed_enabled = models.BooleanField()
    alt_speed_time_begin = models.IntegerField(blank=True)
    alt_speed_time_day = models.IntegerField(blank=True)
    alt_speed_time_enabled = models.BooleanField()
    alt_speed_time_end = models.IntegerField(blank=True)
    alt_speed_up = models.IntegerField(blank=True)
    bind_address_ipv4 = models.GenericIPAddressField()
    bind_address_ipv6 = models.GenericIPAddressField()
    blocklist_enabled = models.BooleanField()
    blocklist_url = models.URLField(max_length=300)
    cache_size_mb = models.IntegerField(blank=True)
    dht_enabled = models.BooleanField()
    download_dir = models.CharField(max_length=200, blank=True)
    download_limit = models.IntegerField(blank=True)
    download_limit_enabled = models.IntegerField(blank=True)
    download_queue_enabled = models.BooleanField()
    download_queue_size = models.IntegerField(blank=True)
    encryption = models.IntegerField(blank=True)
    idle_seeding_limit = models.IntegerField(blank=True)
    idle_seeding_limit_enabled = models.BooleanField()
    incomplete_dir = models.CharField(max_length=200, blank=True)
    incomplete_dir_enabled = models.BooleanField()
    lpd_enabled = models.BooleanField()
    max_peers_global = models.IntegerField(blank=True)
    message_level = models.IntegerField(blank=True)
    peer_congestion_algorithm = models.CharField(max_length=200, blank=True)
    peer_id_ttl_hours = models.IntegerField(blank=True)
    peer_limit_global = models.IntegerField(blank=True)
    peer_limit_per_torrent = models.IntegerField(blank=True)
    peer_port =	models.IntegerField(blank=True)
    peer_port_random_high = models.IntegerField(blank=True)
    peer_port_random_low = models.IntegerField(blank=True)
    peer_port_random_on_start = models.BooleanField()
    peer_socket_tos = models.CharField(max_length=200, blank=True)
    pex_enabled = models.BooleanField()
    port_forwarding_enabled = models.BooleanField()
    preallocation = models.IntegerField(blank=True)
    prefetch_enabled = models.BooleanField()
    queue_stalled_enabled = models.BooleanField()
    queue_stalled_minutes = models.IntegerField(blank=True)
    ratio_limit = models.IntegerField(blank=True)
    ratio_limit_enabled = models.BooleanField()
    rename_partial_files = models.BooleanField()
    rpc_authentication_required = models.BooleanField()
    rpc_bind_address = models.GenericIPAddressField()
    rpc_enabled = models.BooleanField()
    rpc_host_whitelist = models.CharField(max_length=200, blank=True)
    rpc_host_whitelist_enabled = models.BooleanField()
    rpc_password = models.CharField(max_length=200, blank=True)
    rpc_port = models.IntegerField(blank=True)
    rpc_url = models.CharField(max_length=200, blank=True)
    rpc_username = models.CharField(max_length=200, blank=True)
    rpc_whitelist = models.CharField(max_length=200, blank=True)
    rpc_whitelist_enabled = models.BooleanField()
    scrape_paused_torrents_enabled = models.BooleanField()
    script_torrent_done_enabled = models.BooleanField()
    script_torrent_done_filename = models.CharField(max_length=200, blank=True)
    seed_queue_enabled = models.BooleanField()
    seed_queue_size = models.IntegerField(blank=True)
    speed_limit_down = models.IntegerField(blank=True)
    speed_limit_down_enabled = models.BooleanField()
    speed_limit_up = models.IntegerField(blank=True)
    speed_limit_up_enabled = models.BooleanField()
    start_added_torrents = models.BooleanField()
    torrentfiles_enabled = models.BooleanField()
    torrentfiles_dir = models.CharField(max_length=200, blank=True)
    trash_original_torrent_files = models.BooleanField()
    umask = models.IntegerField(blank=True)
    upload_limit = models.IntegerField(blank=True)
    upload_limit_enabled = models.IntegerField(blank=True)
    upload_slots_per_torrent = models.IntegerField(blank=True)
    utp_enabled = models.BooleanField()
    watch_dir = models.CharField(max_length=200, blank=True)
    watch_dir_enabled = models.BooleanField()

    def __str__(self):
        return f"{self.bind_address_ipv4}"

    class Meta:
        verbose_name = 'Transmission Settings'
        verbose_name_plural = 'Transmission Settings'