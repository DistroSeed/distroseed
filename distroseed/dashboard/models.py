from __future__ import unicode_literals
from django.db import models

class Excludes(models.Model):
    phrase = models.CharField(max_length=300)

    def __unicode__(self):
        return "%s" % unicode(self.phrase)

class AutoTorrent(models.Model):
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField(max_length=300)
    excludes = models.ManyToManyField(Excludes,blank=True)

    def __unicode__(self):
        return "%s" % unicode(self.name)
