# -*- coding: utf-8 -*-
import time
from campaigns.foundation.applet import decorators, utils, response
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.management.applet.utils import generate_other_dict_data
from campaigns.management import app_id, models
from django.utils.http import urlquote
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from campaigns.foundation import wechat_api
from django.utils.encoding import smart_unicode, smart_str
import json


def _record_pv(request):
    creation_time = int(time.time())
    url = request.path
    ip = utils.get_ip_from_request(request)
    models.PageView.objects.create(
        url=url,
        ip=ip,
        creationTime=creation_time
    )


def _verify_platform(request, view, *args, **kwargs):
    user_agent = request.META.get(FoundationConst.DJANGO_HTTP_USER_AGENT, '')
    request.CUSTOM = dict()
    # 平台判断
    if user_agent.find(FoundationConst.IDENTITY_WEIXIN) > 0:
        # 微信
        wx_user_openid = request.COOKIES.get(FoundationConst.PLATFORM_WEIXIN_NAME)
        if wx_user_openid is None:
            # 获取完openid
            cookie = {'key': 'openid', 'value': '1234456'}
            utils.put_cookie_to_request(request, cookie)
            pass
        else:
            wx_user = models.WXUser.objects.filter(openid=wx_user_openid).first()
            if wx_user is None:
                pass
            utils.put_dict_data_to_request(request, FoundationConst.RN_PLATFORM, FoundationConst.PLATFORM_WEIXIN)
            utils.put_dict_data_to_request(request, FoundationConst.PLATFORM_WEIXIN_NAME, wx_user)
    else:
        utils.put_dict_data_to_request(request, FoundationConst.RN_PLATFORM, FoundationConst.PLATFORM_DESKTOP)
        utils.put_dict_data_to_request(request, FoundationConst.PLATFORM_IP_NAME, utils.get_ip_from_request(request))
    return view(request, *args, **kwargs)


def platform_verification(view):
    def wrapper(request, *args, **kwargs):
        return _verify_platform(request, view, *args, **kwargs)
    return wrapper


def pv(view):
    def wrapper(request, *args, **kwargs):
        _record_pv(request)
        return view(request, *args, **kwargs)
    return wrapper


def page_render(template_name):
    def wrapper(page_view):
        def wrapped(request, *args, **kwargs):
            return decorators._render_page(request, template_name, generate_other_dict_data(), page_view, *args, **kwargs)
        return wrapped
    return wrapper


def action_render(action_view):
    def wrapper(request, *args, **kwargs):
        return decorators._render_action(request, action_view, *args, **kwargs)
    return wrapper


def _auth_url(redirect_uri, scope='snsapi_userinfo', state=None):
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' % \
          ('wxaacd74076c2a65ff', urlquote(redirect_uri, safe=''), scope, state if state else '')
    return url


def _get_url(request):
    url = 'http://%s%s' % \
          (request.get_host(), smart_str(request.get_full_path()))
    # url = 'http://fanta.kuh5.net/fenda201605/index.html'
    return url

