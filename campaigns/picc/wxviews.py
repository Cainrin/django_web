from django.shortcuts import render, render_to_response
from django.conf import settings
from campaigns.picc.applet.vote import FendaVoteManager
from campaigns.picc.applet import decorators
from django.utils.encoding import smart_unicode, smart_str
import urllib
from django.utils.http import urlquote
from django.http import HttpResponseRedirect


def vote(request):
    vote_manager = FendaVoteManager()
    vote_manager.vote(1, None, '192.168.1.1')


def index(request):
    url = 'http://318e668c6413.ih5.cn/idea/OF-K8j7'
    return HttpResponseRedirect(url)
    return render_to_response('campaigns/fenda201605/WX/index.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def details(request):
    return render_to_response('campaigns/fenda201605/WX/details.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def info(request):
    return render_to_response('campaigns/fenda201605/WX/info.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def tidbits(request):
    return render_to_response('campaigns/fenda201605/WX/tidbits.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def tidbits_open(request):
    return render_to_response('campaigns/fenda201605/WX/tidbits_open.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def make(request):
    return render_to_response('campaigns/fenda201605/WX/make.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def uploadPro(request):
    return render_to_response('campaigns/fenda201605/WX/uploadPro.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def works(request):
    return render_to_response('campaigns/fenda201605/WX/works.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })


def resulted(request):
    return render_to_response('campaigns/fenda201605/WX/resulted.html', {
        'static': '{0}campaigns/fenda201605/WX/'.format(settings.STATIC_URL)
    })
