from django.db.models import *
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render

def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def login(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

def logout(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

def logs(request):
    return render_to_response('logs.html', {}, context_instance=RequestContext(request))

def newdistro(request):
    return render_to_response('newdistro.html', {}, context_instance=RequestContext(request))

def notifications(request):
    return render_to_response('notifications.html', {}, context_instance=RequestContext(request))

def settings(request):
    return render_to_response('settings.html', {}, context_instance=RequestContext(request))

def timeline(request):
    return render_to_response('timeline.html', {}, context_instance=RequestContext(request))
