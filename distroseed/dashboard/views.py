from django.db.models import *
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render

def index(request):
    return render_to_response('index.html', {}, context_instance=RequestContext(request))
