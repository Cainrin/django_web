# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django.conf import settings
from campaigns.fenda201605.applet.vote import FendaVoteManager
from django.utils.encoding import smart_unicode, smart_str
import urllib
from django.utils.http import urlquote
from campaigns.foundation.const import FoundationConst
from campaigns.foundation import wechat_api
import json
from django.http import HttpResponse


def vote(request):
    vote_manager = FendaVoteManager()
    vote_manager.vote(1, None, '192.168.1.1')


def index(request):
    url = 'http://%s%s' % \
          (request.get_host(),smart_str(request.get_full_path()))
    u1 = urllib.quote(smart_unicode(url))
    u2 = urlquote(smart_unicode(url))
    auth_state = request.COOKIES.get(FoundationConst.PLATFORM_AUTH_STATE)
    request.CUSTOM = dict()
    request.CUSTOM[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
    code = request.GET.get('code', None)
    if code is not None:
        res = wechat_api.WechatApi().get_auth_access_token(code)
        openid = res.get('openid', None)
        if openid is not None:
            subscriber = wechat_api.WechatApi().get_subscriber(openid)
            return HttpResponse(json.dumps(subscriber), content_type='application/json')
    return HttpResponse(json.dumps(res), content_type='application/json')

    testlist = ["1", "2"]
    return render_to_response('campaigns/fenda201605/PC/index.html', {
        'static': '{0}campaigns/fenda201605/PC/'.format(settings.STATIC_URL),
        'testList': testlist,
        'code': code
    })


def info(request):
    return render_to_response('campaigns/fenda201605/PC/info.html', {
        'static': '{0}campaigns/fenda201605/PC/'.format(settings.STATIC_URL)
    })


def tidbits(request):
    return render_to_response('campaigns/fenda201605/PC/tidbits.html', {
        'static':'{0}campaigns/fenda201605/PC/'.format(settings.STATIC_URL)
    })


def make(request):
    return render_to_response('campaigns/fenda201605/PC/make.html', {
        'static':'{0}campaigns/fenda201605/PC/'.format(settings.STATIC_URL)
    })


def resetMake(request):
    return render_to_response('campaigns/fenda201605/PC/resetMake.html', {
        'static':'{0}campaigns/fenda201605/PC/'.format(settings.STATIC_URL)
    })


def upload(request):
    return render_to_response('campaigns/fenda201605/PC/upload.html', {
        'static':'{0}campaigns/fenda201605/PC/'.format(settings.STATIC_URL)
    })
	
def works(request):
    return render_to_response('campaigns/fenda201605/PC/works.html', {
        'static':'{0}campaigns/fenda201605/PC/'.format(settings.STATIC_URL)
    })	
