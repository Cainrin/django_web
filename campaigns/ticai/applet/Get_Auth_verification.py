# -*- coding: utf-8 -*-
from campaigns.foundation.applet import decorators, utils, response
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.ticai.applet.uitls import generate_other_dict_data
from campaigns.ticai import app_id, models
from django.utils.http import urlquote
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseServerError, Http404
from campaigns.foundation import wechat_api
from django.utils.encoding import smart_unicode, smart_str
import json


def Auth_url(redirect_uri, scope='snsapi_userinfo', state=None):
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' % \
          ('wxaacd74076c2a65ff', urlquote(redirect_uri, safe=''), scope, state if state else '')
    return url

def Get_url(request):
    url = 'http://%s%s' % \
          (request.get_host(), smart_str(request.get_full_path()))
    # url = 'http://fanta.kuh5.net/fenda201605/index.html'
    return url

def Get_auth(request, view, *args, **kwargs):
    try:
        code = request.GET['code']
    except:
        url = Auth_url(Get_url(request), "snsapi_userinfo")
        return HttpResponseRedirect(url)
    try:
        token_data = wechat_api.WechatApi().get_auth_access_token(code)
    except Exception as e:
        return HttpResponseServerError(e)
    try:
        Access_token = token_data['access_token']
        Openid = token_data['openid']
        usr_info =  wechat_api.WechatApi().get_user_info(Access_token, Openid)
        subscriber = json.loads(json.dumps(usr_info))
    except Exception as e:
        return HttpResponseServerError(e)
    try:
        openid = subscriber['openid']
        nickname = subscriber.get('nickname', None)
        city = subscriber.get('nickname', None)
        gender = int(subscriber.get('gender', 0))
        status = int(subscriber.get('subscribe', 0))
        return view(request, *args, **kwargs)
    except Exception as e:
        return HttpResponseServerError(e)



def _Auth_view(view):
    def __authview(request, *args, **kwargs):
        return Get_auth(request, view, *args, **kwargs)
    return __authview