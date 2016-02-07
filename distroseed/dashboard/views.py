from django.db.models import *
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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
    return render_to_response('index.html', {'username' : request.user,}, context_instance=RequestContext(request))

def logs(request):
    return render_to_response('logs.html', {'username' : request.user,}, context_instance=RequestContext(request))

def newdistro(request):
    return render_to_response('newdistro.html', {'username' : request.user,}, context_instance=RequestContext(request))

def notifications(request):
    return render_to_response('notifications.html', {'username' : request.user,}, context_instance=RequestContext(request))

def settings(request):
    return render_to_response('settings.html', {'username' : request.user,}, context_instance=RequestContext(request))

def timeline(request):
    return render_to_response('timeline.html', {'username' : request.user,}, context_instance=RequestContext(request))
