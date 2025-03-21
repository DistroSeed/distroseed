from django.contrib import admin
from .models import *

admin.site.register(AutoTorrent)
admin.site.register(Excludes)
admin.site.register(Includes)
admin.site.register(TransmissionSetting)