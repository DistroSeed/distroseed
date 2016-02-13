from django.conf.urls import url, include
from django.contrib import admin
import distroseed.dashboard.views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', distroseed.dashboard.views.index, name='index'),
    url(r'^login/$', distroseed.dashboard.views.auth_login, name='login'),
    url(r'^logout/$', distroseed.dashboard.views.auth_logout, name='logout'),
    url(r'^newdistro/$', distroseed.dashboard.views.newdistro, name='newdistro'),
    url(r'^currentdistro/$', distroseed.dashboard.views.currentdistro, name='currentdistro'),
    url(r'^notifications/$', distroseed.dashboard.views.notifications, name='notifications'),
    url(r'^logs/$', distroseed.dashboard.views.logs, name='logs'),
    url(r'^settings/$', distroseed.dashboard.views.settings, name='settings'),
    url(r'^timeline/$', distroseed.dashboard.views.timeline, name='timeline'),
    url(r'^admin/', include(admin.site.urls)),
]
