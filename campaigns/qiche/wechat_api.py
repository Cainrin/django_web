#encoding=utf-8
from campaigns.foundation import models
from campaigns.qiche import app_id
import requests
import simplejson
import urllib
import logging
from wechat_sdk import WechatConf, WechatBasic
import time
import random
import string
import hashlib
from django.utils.encoding import smart_str

log = logging.getLogger('django')
# campaign = models.Campaign.objects.get(pk=app_id)
# appid = campaign.weixin.key
# secret = campaign.weixin.secret
appid = "wxaacd74076c2a65ff"
secret = "812bb69266a141f20c281f8efb5fda47"


class APIError(object):
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


def wx_log_error(APIError):
    log.error('wechat api error: [%s], %s' % (APIError.code, APIError.msg))


class WechatBaseApi(object):

    API_PREFIX = u'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self, api_entry=None):
        conf = WechatConf(
            token='hua_yang_link_589',
            appid=appid,
            appsecret=secret,
            encrypt_mode='compatible',  # 可选项: normal/compatible/safe 分别对应 明文/兼容/安全 模式
        )
        self.we_chat = WechatBasic(conf=conf)
        self.appid = appid
        self.appsecret = secret
        self._access_token = None
        self.api_entry = api_entry or self.API_PREFIX
        self.jsapi_ticket = self.we_chat.get_jsapi_ticket()

    @property
    def access_token(self):
        if not self._access_token:
            token, err = self.we_chat.get_access_token()

            if not err:
                self._access_token = token['access_token']
                return self._access_token
            else:
                return None

        return self._access_token


    # 解析微信返回的json数据，返回相对应的dict
    def _process_response(self, rsp):
        if 200 != rsp.status_code:
            return None, APIError(rsp.status_code, 'http error')
        try:
            content = rsp.json()

        except Exception:
            return None, APIError(9999, 'invalid response')
        if 'errcode' in content and content['errcode'] != 0:
            return None, APIError(content['errcode'], content['errmsg'])

        return content

    def _get(self, path, params=None):
        if not params:
            params = {}

        params['access_token'] = self.access_token

        rsp = requests(self.api_entry + path, params=params)

        return self._process_response(rsp)

    def _post(self, path, data, type='json'):

        header = {'content-type': 'application/json'}

        if '?' in path:
            url = self.api_entry + path + 'access_token=' + self.access_token
        else:
            url = self.api_entry + path + '?' + 'access_token=' + self.access_token

        if 'json' == type:
            data = simplejson.dumps(data, ensure_ascii=False).encode('utf-8')

        rsp = requests.post(url, data, headers=header)

        return self._process_response(rsp)


class WechatApi(WechatBaseApi):

    #返回授权url  scope有两种模式：snsapi_base为静默授权只获取openID；snsapi_userinfo为获取用户基本信息，需要用户手动同意
    def auth_url(self, redirect_uri, scope='snsapi_userinfo', state=None):
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=%s&state=%s#wechat_redirect' % \
              (self.appid, urllib.quote(redirect_uri), scope, state if state else '')
        return url

   # 获取网页授权的access_token,open_id
    def get_auth_access_token(self, code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid': self.appid,
            'secret': self.appsecret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        return self._process_response(requests.get(url, params=params))

    # 获取用户信息
    def get_user_info(self, auth_access_token, openid):
        url = u'https://api.weixin.qq.com/sns/userinfo?'
        params = {
            'access_token': auth_access_token,
            'openid': openid,
            'lang': 'zh_CN'
        }

        return self._process_response(requests.get(url, params=params))

    def get_subscriber(self, openid):
        return self.we_chat.get_user_info(openid,lang='zh_CN')

    def get_sign_package(self, url):
        ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': self.we_chat.get_jsapi_ticket()['jsapi_ticket'],
            'timestamp': self.__create_timestamp(),
            'url': url
        }

        res_string = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
        result = {
            'appId': appid,
            'timestamp': ret['timestamp'],
            'nonceStr': ret['nonceStr'],
            'signature': hashlib.sha1(res_string).hexdigest(),
            'jsapi_ticket': ret['jsapi_ticket']
        }
        return result

    def __create_nonce_str(self):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def _get_url(self, request):
        url = 'http://%s%s' % \
              (request.get_host(), smart_str(request.get_full_path()))
        return url

