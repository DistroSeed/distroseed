import re
import requests
import transmissionrpc
from hurry.filesize import size
from django.db.models import *
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django import forms
from django.utils import timezone
from .forms import AutoTorrentForm, NewAutoTorrentForm
from .models import *

def auth_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('index'))

def auth_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def index(request):
    torrents = []
    tc = transmissionrpc.Client('127.0.0.1', port=9091)
    session_stats = tc.session_stats()
    cumulative_stats = session_stats.cumulative_stats
    uploaded = size(cumulative_stats['uploadedBytes'])
    downloaded = size(cumulative_stats['downloadedBytes'])
    active_torrents = session_stats.activeTorrentCount
    torrent_count = session_stats.torrentCount
    free_space = size(session_stats.download_dir_free_space)
    current_torrents = tc.get_torrents()
    for t in current_torrents:
        percent = t.progress
        name = t.name.replace('.iso','').replace('.img','')
        if 'ubuntu' in name:
            name_array = name.split('-')
            distro = name_array[0].capitalize()
            version = name_array[1]
            if name_array[3] == 'amd64':
                arch = 'x64'
            if name_array[3] == 'i386':
                arch = 'x32'
            type = name_array[2].capitalize() + ' ' + arch
        elif 'centos' in name.lower():
            name_array = name.split('-')
            distro = name_array[0]
            version = name_array[1]
            if name_array[3] == 'x86_64':
                arch = 'x64'
            if name_array[3] == 'x86':
                arch = 'x32'
            type = name_array[3].capitalize() + ' ' + arch
        elif 'fedora' in name.lower():
            name_array = name.split('-')
            distro = name_array[0]
            try:
                version = name_array[4] + ' ' + name_array[5]
            except:
                version = name_array[4]
            if name_array[3] == 'x86_64':
                arch = 'x64'
            if name_array[3] == 'x86':
                arch = 'x32'
            if name_array[3] == 'i686':
                arch = 'x32'
            type = name_array[1] + ' ' + name_array[2].capitalize() + ' ' + arch
        else:
            name_array = name.split('-')
            distro = name_array[0].capitalize()
            version = 'unknown'
            arch = 'unknown'
            type = 'unknown'

        dic = {
            'name' : t.name,
            'distro' : distro,
            'version' : version,
            'type' : type,
            'size' : size(t.sizeWhenDone),
            'upload' : size(t.rateUpload),
            'download' : size(t.rateDownload),
            'percent' : percent,
        }
        torrents.append(dic)
    return render_to_response('index.html', {
        'username' : request.user, 
        'torrents' : torrents,
        'uploaded' : uploaded,
        'downloaded' : downloaded,
        'active_torrents' : active_torrents,
        'torrent_count' : torrent_count,
        'free_space' : free_space,
    }, context_instance=RequestContext(request))

def logs(request):
    return render_to_response('logs.html', {'username' : request.user,}, context_instance=RequestContext(request))

def newdistro(request):
    if request.method == "POST":
        form = NewAutoTorrentForm(request.POST)
              
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            form.save_m2m()
            link = AutoTorrent.objects.get(id=model_instance.id).url
            exclude_list = AutoTorrent.objects.get(id=model_instance.id).excludes.all().values_list('phrase', flat=True)
            r = requests.get(link, verify=False)
            data = [x[1] for x in re.findall('(src|href)="(\S+)"',r.content)]
            links = filter(lambda x:x.endswith(".torrent"), data)
            torrent_links = [link + l if 'http' not in l else l for l in links]
            torrent_links = [l for l in torrent_links if not any(ex.lower() in l.lower() for ex in exclude_list)]
            for torrent in torrent_links:
                filedl = requests.get(torrent, stream=True, verify=False)
                with open('/data/downloads/torrents/' + torrent.split('/')[-1], 'wb') as f:
                    for chunk in filedl.iter_content(chunk_size=1024): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)

            return HttpResponseRedirect(reverse('newdistro'))
  
    form = NewAutoTorrentForm()
    return render_to_response('newdistro.html', {
        'username' : request.user,
        'form' : form,
    }, context_instance=RequestContext(request))

def currentdistro(request):
    if request.method == "POST":
        instance = AutoTorrent.objects.get(id=request.POST['id'])
        form = AutoTorrentForm(request.POST or None, instance=instance)
              
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            form.save_m2m()
            link = AutoTorrent.objects.get(id=model_instance.id).url
            exclude_list = AutoTorrent.objects.get(id=model_instance.id).excludes.all().values_list('phrase', flat=True)
            r = requests.get(link, verify=False)
            data = [x[1] for x in re.findall('(src|href)="(\S+)"',r.content)]
            links = filter(lambda x:x.endswith(".torrent"), data)
            torrent_links = [link + l if 'http' not in l else l for l in links]
            torrent_links = [l for l in torrent_links if not any(ex.lower() in l.lower() for ex in exclude_list)]
            for torrent in torrent_links:
                filedl = requests.get(torrent, stream=True, verify=False)
                with open('/data/downloads/torrents/' + torrent.split('/')[-1], 'wb') as f:
                    for chunk in filedl.iter_content(chunk_size=1024): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)

            return HttpResponseRedirect(reverse('currentdistro'))
  
    forms = []
    current_autotorrents = AutoTorrent.objects.all()
    for torrent in current_autotorrents:
        forms.append(AutoTorrentForm(None, instance=torrent))
    return render_to_response('currentdistro.html', {
        'username' : request.user,
        'forms': forms
    }, context_instance=RequestContext(request))

def notifications(request):
    return render_to_response('notifications.html', {'username' : request.user,}, context_instance=RequestContext(request))

def settings(request):
    return render_to_response('settings.html', {'username' : request.user,}, context_instance=RequestContext(request))

def timeline(request):
    return render_to_response('timeline.html', {'username' : request.user,}, context_instance=RequestContext(request))
