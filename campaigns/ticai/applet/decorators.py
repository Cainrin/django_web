# -*- coding: utf-8 -*-
import time, xlwt, StringIO
from campaigns.foundation.applet import decorators, utils, response
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.ticai.applet.uitls import generate_other_dict_data
from campaigns.ticai import app_id, models
from django.utils.http import urlquote
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from campaigns.ticai import wechat_api
from django.utils.encoding import smart_unicode, smart_str
import json, datetime


def _record_pv(request):
    pv = models.CountPUV.objects.get(id=1)
    count = int(pv.pv) + 1
    models.CountPUV.objects.filter(id=1).update(pv=str(count))


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
          ('wx09a6ae929e7445a8', urlquote(redirect_uri, safe=''), scope, state if state else '')
    return url

def _wechat_sport():
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx7fa037cc7dfabad5&redirect_uri=http%3a%2f%2fhw.weixin.qq.com%2f" \
          "steprank%2fauth%3fappid%3d%26scope%3dsnsapi_health_realtime&respo" \
          "nse_type=code&scope=snsapi_base&state=&connect_redirect=1#wechat_redirect"
    return url

def _get_url(request):
    url = 'http://%s%s' % \
          (request.get_host(), smart_str(request.get_full_path()))
    # url = 'http://fanta.kuh5.net/fenda201605/index.html'
    return url


def _Verify_Auth(request, view, *args, **kwargs):
    user_agent = request.META.get(FoundationConst.DJANGO_HTTP_USER_AGENT, '')
    # 平台判断
    if user_agent.find(FoundationConst.IDENTITY_WEIXIN) > 0:
        # 判读是否经过网页授权，init和None表示未执行，process表示由微信重定向回来，finish表示已授权
        auth_state = request.session.get(FoundationConst.PLATFORM_AUTH_STATE)
        if auth_state == "finish":
            auth_state = "syn"
        if request.session.get("day") != str(datetime.date.today()):
            nowday = datetime.date.today()
            request.session['day'] = str(nowday)
            auth_state = "syn"
        if auth_state is None or auth_state == "syn":
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = "init"
            url = _wechat_sport()
            return HttpResponseRedirect(url)
        if auth_state is None or auth_state == 'init':
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
            url = _auth_url(_get_url(request), "snsapi_base")
            return HttpResponseRedirect(url)
        elif auth_state == 'process':
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'init'
            code = request.GET.get('code')
            if code is None:
                request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                url = _auth_url(_get_url(request), "snsapi_base")
                return HttpResponseRedirect(url)
            else:
                    res = wechat_api.WechatApi().get_auth_access_token(code)
                    request.session['walkCount'] = res['access_token']
            try:
                openid = res['openid']
            except Exception as e:
                # raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_AUTH_OPENID_WEIXIN, str(e)))
                return str(e)
            # 将openid存入session
            request.session[FoundationConst.PLATFORM_WEIXIN_NAME] = openid
            # 添加微信用户信息入库
            wx_user = models.WXUser.objects.filter(openid=openid).first()
            if wx_user is None:
                # subscriber = json.loads(json.dumps(wechat_api.WechatApi().get_subscriber(openid)))
                try:
                    sub_openid = openid
                    nickname = None
                    city = None
                    gender = 0
                    status = 0
                except Exception as e:
                    raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
                uv = models.CountPUV.objects.filter(id=1)
                models.CountPUV.objects.filter(id=1).update(uv=int(uv[0].uv) + 1)

                models.WXUser.objects.create(
                    openid=sub_openid,
                    gender=gender,
                    status=status
                )
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'finish'
        else:
            wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_NAME)
            if wx_user_openid is None:
                request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                url = _auth_url(_get_url(request), "snsapi_base")
                return HttpResponseRedirect(url)
            else:
                wx_user = models.WXUser.objects.filter(openid=wx_user_openid).first()
                if wx_user is None:
                    request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                    url = _auth_url(_get_url(request), "snsapi_base")
                    return HttpResponseRedirect(url)
    else:
        url = _auth_url(_get_url(request), "snsapi_base")
        return HttpResponseRedirect(url)
    return view(request, *args, **kwargs)




#  微信弱授权
def _verify_auth(request, view, *args, **kwargs):
    user_agent = request.META.get(FoundationConst.DJANGO_HTTP_USER_AGENT, '')
    # 平台判断
    if user_agent.find(FoundationConst.IDENTITY_WEIXIN) > 0:
        # 判读是否经过网页授权，init和None表示未执行，process表示由微信重定向回来，finish表示已授权
        auth_state = request.session.get(FoundationConst.PLATFORM_AUTH_STATE)
        if auth_state is None or auth_state == 'init':
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
            url = _auth_url(_get_url(request), "snsapi_base")
            return HttpResponseRedirect(url)
        elif auth_state == 'process':
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'init'
            code = request.GET.get('code')
            if code is None:
                request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                url = _auth_url(_get_url(request), "snsapi_base")
                return HttpResponseRedirect(url)
            else:
                    res = wechat_api.WechatApi().get_auth_access_token(code)
                    request.session['walkCount'] = res['access_token']
            try:
                openid = res['openid']
            except Exception as e:
                # raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_AUTH_OPENID_WEIXIN, str(e)))
                return str(e)
            # 将openid存入session
            request.session[FoundationConst.PLATFORM_WEIXIN_NAME] = openid
            # 添加微信用户信息入库
            wx_user = models.WXUser.objects.filter(openid=openid).first()
            if wx_user is None:
                # subscriber = json.loads(json.dumps(wechat_api.WechatApi().get_subscriber(openid)))
                try:
                    sub_openid = openid
                    nickname = None
                    city = None
                    gender = 0
                    status = 0
                except Exception as e:
                    raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))

                models.WXUser.objects.create(
                    openid=sub_openid,
                    gender=gender,
                    status=status
                )
            request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'finish'
        else:
            wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_NAME)
            if wx_user_openid is None:
                request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                url = _auth_url(_get_url(request), "snsapi_base")
                return HttpResponseRedirect(url)
            else:
                wx_user = models.WXUser.objects.filter(openid=wx_user_openid).first()
                if wx_user is None:
                    request.session[FoundationConst.PLATFORM_AUTH_STATE] = 'process'
                    url = _auth_url(_get_url(request), "snsapi_base")
                    return HttpResponseRedirect(url)
    else:
        url = _auth_url(_get_url(request), "snsapi_base")
        return HttpResponseRedirect(url)
    return view(request, *args, **kwargs)


def exportExcel(request, name, dict1):
    response = HttpResponse(content_type='application/vnd.ms-excel', charset='UTF-8')
    filename = 'attachment;filename=' + str(name) + ".xls"
    response['Content-Disposition'] = filename
    wb = xlwt.Workbook(encoding='utf-8')
    _lenght = len(dict1[0])                             # 获取传入dict长度
    sheet = wb.add_sheet(u"数据表")
    for i, t in zip(range(0, _lenght), dict1[0]):            # 获取dict key个数 以及键填写
        sheet.write(0, i, t)
    row = 1
    count = 0
    Len = len(dict1)
    while count < Len:
        _LENT = len(dict1[count].values())
        for i, t in zip(range(0, _LENT), dict1[count].values()):
            sheet.write(row, i, t)
        count += 1
        row += 1
    output = StringIO.StringIO()
    wb.save(output)
    output.seek(0)
    response.write(output.getvalue())
    return response

# 授权验证
def auth_verification(view):
    def auth(request, *args, **kwargs):
        return _verify_auth(request, view, *args, **kwargs)
    return auth


def Auth_Verification(view):
    def auth(request, *args, **kwargs):
        return _Verify_Auth(request, view, *args, **kwargs)
    return auth

