# -*- coding: utf-8 -*-
import json, time
from django import http
from campaigns.foundation.const import DisplayConst, FoundationConst
from campaigns.foundation.applet import utils, response, access
from campaigns.yiquan import models
from django.utils.http import urlquote
from django.http import HttpResponseRedirect, HttpResponse
from campaigns.foundation import wechat_api
from Get_Auth_verification import *

def _record_pv(request):
    creation_time = int(time.time())
    url = request.path
    ip = utils.get_ip_from_request(request)
    models.PageView.objects.create(
        url=url,
        ip=ip,
        creationTime=creation_time
    )


def _Verify_platform(request, view, *args, **kwargs):
    user_agent = request.META.get(FoundationConst.DJANGO_HTTP_USER_AGENT, '')
    request.CUSTOM = dict()
    # 平台判断
    if user_agent.find(FoundationConst.IDENTITY_WEIXIN) > 0:
        # 微信
        wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
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
            utils.put_dict_data_to_request(request, FoundationConst.PLATFORM_WEIXIN_OPENID, wx_user)
    else:
        utils.put_dict_data_to_request(request, FoundationConst.RN_PLATFORM, FoundationConst.PLATFORM_DESKTOP)
        utils.put_dict_data_to_request(request, FoundationConst.PLATFORM_IP_NAME, utils.get_ip_from_request(request))
    return view(request, *args, **kwargs)


def _record_pv_uv(request, app_id):
    creation_time = int(time.time())
    url = request.path
    ip = utils.get_ip_from_request(request)
    rs = access.redis_session()
    # pv
    list_name = '{0}:{1}'.format(FoundationConst.REDIS_LIST_PV, app_id)
    value = {FoundationConst.RN_URL: url, FoundationConst.RN_CREATION_TIME: creation_time, FoundationConst.RN_IP: ip}
    rs.rpush(list_name, json.dumps(value))
    # uv
    wx_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
    if wx_openid is not None:
        list_name = '{0}:{1}'.format(FoundationConst.REDIS_LIST_UV, app_id)
        value = {FoundationConst.PLATFORM_WEIXIN_OPENID: wx_openid, FoundationConst.RN_URL: url, FoundationConst.RN_CREATION_TIME: creation_time, FoundationConst.RN_IP: ip}
        rs.rpush(list_name, json.dumps(value))


def _render_page(request, template_name, other_dict_data, page_view, *args, **kwargs):
    try:
        rd = page_view(request, *args, **kwargs)
        cookie_list = utils.get_cookie_list_from_request(request)
        if isinstance(rd, dict):
            if other_dict_data is not None:
                rd.update(other_dict_data)
            return response.page_success(template_name, rd, cookie_list)
        elif rd is None:
            return response.page_success(template_name, other_dict_data, cookie_list)
        elif isinstance(rd, http.HttpResponse):
            return rd
        else:
            raise utils.ServerException(DisplayConst.EXCEPTION_SERVER_NOT_STD_BEHAVIOUR)
    except Exception as e:
        client_error_dict = {DisplayConst.ERROR_MESSAGE: str(e)}
        if isinstance(e, utils.ClientException):
            return response.page_400(DisplayConst.PAGE_400, client_error_dict)
        elif isinstance(e, utils.ServerException):
            return response.page_500(DisplayConst.PAGE_500, client_error_dict)
        else:
            return response.page_501(DisplayConst.PAGE_501, client_error_dict)


def _render_action(request, action_view, *args, **kwargs):
    try:
        rd = action_view(request, *args, **kwargs)
        cookie_list = utils.get_cookie_list_from_request(request)
        if isinstance(rd, dict):
            return response.action_success(rd, cookie_list)
        elif rd is None:
            return response.action_success(dict(), cookie_list)
        elif isinstance(rd, http.HttpResponse):
            return rd
        else:
            raise utils.ServerException(DisplayConst.EXCEPTION_SERVER_NOT_STD_BEHAVIOUR)
    except Exception as e:
        client_error_dict = {DisplayConst.ERROR_MESSAGE: str(e)}
        if isinstance(e, utils.ClientException):
            return response.action_400(client_error_dict)
        elif isinstance(e, utils.ServerException):
            return response.action_500(client_error_dict)
        else:
            return response.action_501(client_error_dict)

#微信弱授权验证流程
def _verify_auth(request, view, *args, **kwargs):
    user_agent = request.META.get(FoundationConst.DJANGO_HTTP_USER_AGENT, '')
    # 平台判断
    if user_agent.find(FoundationConst.IDENTITY_WEIXIN) > 0:
        # 判读是否经过网页授权，init和None表示未执行，process表示由微信重定向回来，finish表示已授权
        auth_state = request.session.get(FoundationConst.PLATFORM_AUTH_STATE)
        if auth_state is None or auth_state == 'init':
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
            url = Auth_url(Get_url(request), "snsapi_base")
            return HttpResponseRedirect(url)
        elif auth_state == 'process':
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'init'
            try:
                code = request.GET['code']
            except Exception as e:
                raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_AUTH_CODE_WEIXIN, str(e)))
            res = wechat_api.wechatAPI.get_auth_access_token(code)
            try:
                openid = res['openid']
            except Exception as e:
                raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_AUTH_OPENID_WEIXIN, str(e)))
            # 将openid存入session
            request.session[FoundationConst.PLATFORM_WEIXIN_OPENID] = openid
            # 添加微信用户信息入库
            wx_user = models.WXUser.objects.filter(openid=openid).first()
            if wx_user is None:
                subscriber = json.loads(json.dumps(wechat_api.wechatAPI.get_subscriber(openid)))
                try:
                    sub_openid = subscriber['openid']
                    nickname = subscriber.get('nickname', None)
                    city = subscriber.get('city', None)
                    gender = int(subscriber.get('sex', 0))
                    status = int(subscriber.get('subscribe', 0))
                except Exception as e:
                    raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))

                models.WXUser.objects.create(
                    openid=sub_openid,
                    gender=gender,
                    status=status
                )
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'finish'
        else:
            wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
            if wx_user_openid is None:
                request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                url = Auth_url(Get_url(request), "snsapi_base")
                return HttpResponseRedirect(url)
            else:
                wx_user = models.WXUser.objects.filter(openid=wx_user_openid).first()
                if wx_user is None:
                    request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                    url = Auth_url(Get_url(request), "snsapi_base")
                    return HttpResponseRedirect(url)
    return view(request, *args, **kwargs)


# 强授权验证流程
def Power_verify_auth(request, view, *args, **kwargs):
    # 判读是否经过网页授权，init和None表示未执行，process表示由微信重定向回来，finish表示已授权
    auth_state = request.session.get(FoundationConst.PLATFORM_AUTH_STATE)
    if auth_state is None or auth_state == 'init':
        request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
        url = Auth_url(Get_url(request), "snsapi_userinfo")
        return HttpResponseRedirect(url)
    elif auth_state == 'process':
        #Get_auth(request, view, *args, **kwargs)
        try:
            print request
            code = request.GET.get('code')
        except:
            url = Auth_url(Get_url(request), 'snsapi_userinfo')
            return HttpResponseRedirect(url)
        if code is None:
            url = Auth_url(Get_url(request), "snsapi_userinfo")
            return HttpResponseRedirect(url)
        res = wechat_api.wechatAPI.get_auth_access_token(code)
        try:
            Access_token = res['access_token']
            Openid = res['openid']
            request.session[FoundationConst.PLATFORM_WEIXIN_OPENID] = Openid
            usr_info =  wechat_api.wechatAPI.get_user_info(Access_token, Openid)
            subscriber = usr_info
        except Exception as e:
            return HttpResponseServerError(e)
        try:
            dbcreate = models.WXUser.objects.create(
                openid=Openid,
                nickname=subscriber['nickname'].encode('raw_unicode_escape'),
                city=(subscriber['city']).encode('raw_unicode_escape'),
                fixstatus=1,
                gender=int(subscriber['sex'])
            )
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'finish'
        except Exception as e:
            return HttpResponseServerError(e)
    else:
        openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
        if openid is None:
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
            url = Auth_url(Get_url(request), "snsapi_userinfo")
            return HttpResponseRedirect(url)
        # 如果数据库中没有存储微信用户信息，强授权重新获取
        wx_user = models.WXUser.objects.filter(openid=openid).first()
        if wx_user is None:
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
            url = Auth_url(Get_url(request), "snsapi_userinfo")
            return HttpResponseRedirect(url)
        pass
    return view(request, *args, **kwargs)


#弱授权验证
def S_verify_auth(view):
    def _auth(request, *args, **kwargs):
        return _verify_auth(request, view, *args, **kwargs)
    return _auth

#强授权验证
def P_verify_auth(view):
    def _Auth(request, *args, **kwargs):
        return Power_verify_auth(request, view, *args, **kwargs)
    return _Auth

#平台判断
def Platform_verification(view):
    def wrapper(request, *args, **kwargs):
        return _Verify_platform(request, view, *args, **kwargs)
    return wrapper

#renderpage
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


# 计算pv
def pv(view):
    def wrapper(request, *args, **kwargs):
        _record_pv(request)
        return view(request, *args, **kwargs)
    return wrapper