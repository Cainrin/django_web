# -*- coding: utf-8 -*-
from campaigns.ycblank.applet.decorators import page_render, auth_verification, pv
from campaigns.ycblank.config import ViewConfig
import models
import jpype, json
from django.http import HttpResponseRedirect
from campaigns.ycblank.applet.Get_Auth_verification import _Auth_view
from campaigns.ycblank.applet.decorators import P_verify_auth



@pv
@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "index.html")
def index(request):
    user = request.GET.get("user", None)
    print user
    if user is None:
        return HttpResponseRedirect('error.html')
    else:
        secert = "zIe4q3zg9khpIl8tEuj83jr1UWxsah6juiy48mxK1DVTkee4aiSPJrRPR71SGuCt"
        jarpath = '/tmp'
        isTurnOn = jpype.isJVMStarted()
        if isTurnOn == 0:
            jpype.startJVM(jpype.getDefaultJVMPath(), "-Djava.ext.dirs=%s" % jarpath)
        Test = jpype.JClass("cn.com.yitong.util.security.ThreeDes")
        str_json = Test.getDec(user, secert)
        print str_json
        str_dict = json.loads(str_json)
        print str_dict
        openid = str_dict['openid']
        nickname = str_dict['nickname']
        print openid, nickname
        request.session['wxUser'] = openid
        usrInfo = models.WXUser.objects.filter(openid=openid).first()
        if usrInfo is None:
            models.WXUser.objects.create(openid=openid, nickname=nickname, gender=0, status=0)


@page_render(ViewConfig.TEMPLATE_MOBILE_URL + "error.html")
def lbs_back(request):
    pass


@page_render(ViewConfig.TEMPLATE_PC_URL + "ccy.html")
def lbs_ccy(request):
    pass