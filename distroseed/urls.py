"""distroseed URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
import distroseed.dashboard.views

urlpatterns = [
    url(r'^$', distroseed.dashboard.views.index, name='index'),
    url(r'^login/$', distroseed.dashboard.views.auth_login, name='login'),
    url(r'^logout/$', distroseed.dashboard.views.auth_logout, name='logout'),
    url(r'^newdistro/$', distroseed.dashboard.views.newdistro),
    url(r'^notifications/$', distroseed.dashboard.views.notifications),
    url(r'^logs/$', distroseed.dashboard.views.logs),
    url(r'^settings/$', distroseed.dashboard.views.settings),
    url(r'^timeline/$', distroseed.dashboard.views.timeline),
]
