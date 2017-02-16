# -*- coding: utf-8 -*-
import math, datetime, pytz, random
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.meeting import models, config, const
from campaigns.foundation import wechat_api
from campaigns.meeting.applet import decorators
from campaigns.meeting.applet.vote import FendaVoteManager
from campaigns.meeting.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos
from django.utils import timezone
from collections import Counter
from campaigns.meeting.applet.Tcos import Auth
from campaigns.meeting.applet.getLocation import txLocations
import numpy



@decorators.action_render
def get_sign_package(request):
    try:
        url = request.POST['url']
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    sign_package = wechat_api.WechatApi().get_sign_package(url)
    return sign_package




@decorators.action_render
def checkBlind(request):
    try:
        openid = request.session.get("wxUser")
        info = models.met_Author.objects.filter(openid=openid).first()
        if info is None:
            return {"result_code": 1, "result_msg": "未绑定"}
        else:
            return {"result_code": 0, "result_msg": "已绑定"}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}




@decorators.action_render
def infoCache(request):
    try:
        phoneNum = request.POST['phone']
        openid = request.session.get("wxUser")
        info = models.met_Author.objects.filter(phoneNum=phoneNum)
        if info:
            info.update(openid=openid)
            return {"reuslt_code": 0, "result_msg": "绑定成功", "name": info[0].name, "img": info[0].headimg}
        else:
            return {"reuslt_code": 1, "result_msg": "该号码已被人绑定"}
    except Exception as e:
        return {"reuslt_code": -1, "result_msg": str(e)}


@decorators.action_render
def readMsg(request):
    try:
        l1 = []
        msgList = models.met_Message.objects.filter(isread=0).all()
        for i in msgList:
            d1 = {}
            d1['name'] = models.met_Author.objects.filter(openid=i.openid).first().name
            d1['phone'] = models.met_Author.objects.filter(openid=i.openid).first().phoneNum
            d1['headimg'] = models.met_Author.objects.filter(openid=i.openid).first().headimg
            d1['msg'] = i.msg
            l1.append(d1)
        msgList.update(isread=1)
        return {"result_code": 0, "result_msg": None, "msgList": l1}
    except Exception as e:
        return {'result_code': -1, "result_msg": str(e)}




@decorators.action_render
def sendMsg(request):
    try:
        msg = request.POST['msg']
        openid = request.session.get("wxUser")
        models.met_Message.objects.create(
            msg=msg,
            openid=openid
        )
        return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


@decorators.action_render
def hitPrize(request):
    try:
        l1 = []
        priceUser = models.met_hitprice.objects.all()
        for i in priceUser:
            l1.append(i.openid)
        l2 = []
        msgUser = models.met_Message.objects.filter(isSend=1, isread=0).all()
        for i in msgUser:
            l2.append(i.openid)
        msgUser.update(isSend=0)
        l3 = set(l2) - set(l1)
        hituserOpenid = l3[random.randint(0, len(l3))]
        hitUsr = models.met_Author.objects.filter(openid=hituserOpenid).first().name
        headimg = models.met_Author.objects.filter(openid=hituserOpenid).first().headimg
        models.met_hitprice.objects.create(openid=hituserOpenid)
        l4 = []
        for i in l3:
            d1 = {}
            info = models.met_Author.objects.filter(openid=i).first()
            d1['name'] = info.name
            d1['headimg'] = info.headimg
            l4.append(d1)
        return {"result_code": 0, "result_msg": None, "hitUsr": hitUsr, "headimg": headimg, "list": l4}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


@decorators.action_render
def saveTcload(request):
    name = request.GET['name']
    img = request.GET['img']
    phoneNum = request.GET['phone']
    models.met_Author.objects.create(
        name=name,
        headimg=img,
        phoneNum=phoneNum,
    )
    return {"result_code": 0, "result_msg": "success"}