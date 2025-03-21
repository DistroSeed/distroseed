import re
import ast
import json
import requests
import subprocess
import transmissionrpc
from bs4 import BeautifulSoup
from hurry.filesize import size
from urllib.parse import urljoin
from django.db.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings
from .forms import AutoTorrentForm, NewAutoTorrentForm, TransmissionSettingForm, ExcludesForm, IncludesForm,DeletePhraseForm
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
    tc = transmissionrpc.Client(
        settings.TRANSMISSION_HOST,
        port=settings.TRANSMISSION_PORT,
        user=settings.TRANSMISSION_USER,
        password=settings.TRANSMISSION_PASSWORD
    )
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
        name = t.name
        distro = 'unknown'
        version = 'unknown'
        arch = 'unknown'
        dist_type = 'unknown'
        if 'ubuntu' in name.lower():
            distro = "Ubuntu"
        elif 'centos' in name.lower():
            distro = "CentOS"
        elif 'fedora' in name.lower():
            distro = "Fedora"
        elif 'raspbian' in name.lower():
            distro = "Raspbian"
        elif 'archlinux' in name.lower():
            distro = "ArchLinux"
        elif 'kali' in name.lower():
            distro = "Kali"
        elif 'slackware' in name.lower():
            distro = "Slackware"
        elif 'debian' in name.lower():
            distro = "Debian"
        elif 'mint' in name.lower() or 'lmde' in name.lower():
            distro = "Linux Mint"
        elif 'tails' in name.lower():
            distro = "Tails"
        elif 'opensuse' in name.lower():
            distro = "OpenSUSE"
        # Arch statements
        if 'x86_64' in name.lower():
            arch = 'x64'
        elif 'amd64' in name.lower():
            arch = 'x64'
        elif 'x86' in name.lower():
            arch = 'x32'
        elif 'i686' in name.lower():
            arch = 'x32'
        elif 'dual' in name.lower():
            arch = 'x32 & x64'
        elif 'i386' in name.lower():
            arch = 'x32'
        elif 'armel' in name.lower():
            arch = 'ARMEL'
        elif 'armhf' in name.lower():
            arch = 'ARMHF'
        elif '64bit' in name.lower():
            arch = 'x64'
        elif '32bit' in name.lower():
            arch = 'x32'
        # version grab
        # Regular expression to extract versions
        pattern = r'\d+\.\d+(\.\d+)?'
        version_str = re.search(pattern, name.lower())
        if version_str:
            version = version_str.group()
        if version == "unknown":
            pattern = r'(\d+)$'
            version_str = re.search(pattern, name.lower())
            if version_str:
                version = version_str.group()
        # get distro type
        if "desktop" in name.lower():
            dist_type = "Desktop"
        elif "server" in name.lower():
            dist_type = "Server"
        elif "live" in name.lower():
            dist_type = "Live"
        elif "everything" in name.lower():
            dist_type = "Everything"
        elif "netinst" in name.lower():
            dist_type = "Network Installer"
        elif "cinnamon" in name.lower():
            dist_type = "Cinnamon"
        elif "mate" in name.lower():
            dist_type = "MATE"
        elif "xfce" in name.lower():
            dist_type = "Xfce"
        elif "installer" in name.lower():
            dist_type = "Installer"
        elif "img" in name.lower():
            dist_type = "IMG"
        elif "dvd" in name.lower():
            dist_type = "DVD"
        elif "iso" in name.lower():
            dist_type = "ISO"
        dic = {
            'name' : t.name,
            'distro' : distro,
            'version' : version,
            'type' : dist_type,
            'arch' : arch,
            'size' : size(t.sizeWhenDone),
            'upload' : size(t.rateUpload),
            'download' : size(t.rateDownload),
            'percent' : percent,
        }
        torrents.append(dic)
    return render(request, 'index.html', {
        'username' : request.user, 
        'torrents' : torrents,
        'uploaded' : uploaded,
        'downloaded' : downloaded,
        'active_torrents' : active_torrents,
        'torrent_count' : torrent_count,
        'free_space' : free_space,
    })

def logs(request):
    return render(request,'logs.html', {'username' : request.user})

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
            include_list = AutoTorrent.objects.get(id=model_instance.id).includes.all().values_list('phrase', flat=True)
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

            return HttpResponseRedirect(reverse('currentdistro'))
  
    forms = []
    current_autotorrents = AutoTorrent.objects.all()
    for torrent in current_autotorrents:
        forms.append(AutoTorrentForm(None, instance=torrent))
    form = NewAutoTorrentForm()
    return render(request,'currentdistro.html', {
        'username' : request.user,
        'forms': forms,
        'form': form,
    })

def tc_settings(request):
    if request.method == "POST":
        instance = TransmissionSetting.objects.get(id=request.POST['id'])
        form = TransmissionSettingForm(request.POST, instance=instance)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            qs = json.dumps(ast.literal_eval(re.sub("_", "-", str(TransmissionSetting.objects.last().values()))))
            transmissionobj = json.loads(qs)
            # TODO: fix the process to run as a foreground process
            subprocess.call(['pkill', '-f', 'transmission-daemon'])
            with open('/etc/transmission-daemon/settings.json', 'w') as f:
                json.dump(transmissionobj, f, indent=4, sort_keys=True)
            subprocess.call(['transmission-daemon', '--log-level=debug', '--config-dir', '/etc/transmission-daemon', '--foreground', '&'])
        return HttpResponseRedirect(reverse('settings'))
            
    current_settings = TransmissionSetting.objects.last()
    form = TransmissionSettingForm(None, instance=current_settings)
    return render(request,'settings.html', {'username' : request.user, 'form': form,})

def manage_phrases(request):
    if request.method == "POST":
        excludes_form = ExcludesForm(request.POST)
        includes_form = IncludesForm(request.POST)
        delete_form = DeletePhraseForm(request.POST)

        if 'add_exclude' in request.POST and excludes_form.is_valid():
            excludes_form.save()

        if 'add_include' in request.POST and includes_form.is_valid():
            includes_form.save()

        if 'delete_phrase' in request.POST and delete_form.is_valid():
            phrase_id = delete_form.cleaned_data['phrase_id']
            model_type = request.POST.get('model_type')

            if model_type == "excludes":
                phrase = get_object_or_404(Excludes, id=phrase_id)
            elif model_type == "includes":
                phrase = get_object_or_404(Includes, id=phrase_id)
            else:
                phrase = None

            if phrase:
                phrase.delete()

        return redirect('managephrases')  # Replace with the correct URL name
    
    else:
        excludes_form = ExcludesForm()
        includes_form = IncludesForm()
        delete_form = DeletePhraseForm()
        excludes_list = Excludes.objects.all()
        includes_list = Includes.objects.all()
    
    return render(request, 'manage_phrases.html', {
        'username' : request.user, 
        'excludes_form': excludes_form,
        'includes_form': includes_form,
        'delete_form': delete_form,
        'excludes_list': excludes_list,
        'includes_list': includes_list
    })

def restart_transmission(request):
    try:
        # Stop Transmission Daemon
        subprocess.run(["pkill", "transmission-daemon"], check=True)

        # Start Transmission Daemon
        subprocess.run(["transmission-daemon", "--config-dir", "/root/.config/transmission-daemon"], check=True)

        return JsonResponse({"status": "success", "message": "Transmission Daemon restarted."})
    except subprocess.CalledProcessError as e:
        return JsonResponse({"status": "error", "message": str(e)})