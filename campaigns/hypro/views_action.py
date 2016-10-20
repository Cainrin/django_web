# -*- coding: utf-8 -*-
import math, datetime, pytz, random
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.hypro import models, config, const, wechat_api
from campaigns.hypro.applet import decorators
from campaigns.hypro.applet.vote import FendaVoteManager
from campaigns.hypro.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos
from django.utils import timezone
from collections import Counter
from campaigns.hypro.applet.Tcos import Auth




@decorators.action_render
def get_sign_package(request):
    try:
        url = request.POST['url']
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    sign_package = wechat_api.WechatApi().get_sign_package(url)
    return sign_package




@decorators.action_render
def exportExcel(request):
    try:
        l2 = []
        l1 = []
        l3 = []
        pvData = models.PageView.objects.all().order_by("creationTime")             # 按照时间排序获得pv所有数据
        uvData = models.UniqueVisitor.objects.all().order_by("creationTime")        # 按照时间排序获得uv所有数据
        for u in uvData:
            l2.append(u.creationTime)
        for i in pvData:
            l1.append(i.creationTime)
        d1 = dict(Counter(l1))                                                     # counter计数模块返回列表中同元素出现次数
        d2 = dict(Counter(l2))
        for i, j, d in d1.keys(), d1.values(), d2.values():
            d3 = {}
            d3['date'] = i,
            d3['pv'] = j
            d3['uv'] = d
            l3.append(d3)
        exPorter = decorators.exportExcel(request=request, name="每日PUV", dict1=l3)
        return exPorter
    except Exception as e:
        return {"result_code": 1, "result_msg": None}


@decorators.action_render
def tocloud(request):
    try:
        sign_type = request.GET.get("sign_type", None)
        if sign_type == "appSign":
            expired = request.GET.get("expired", None)
            bucketName = request.GET.get("bucketName", None)
            if expired is None or bucketName is None:
                return {"code": 10001, "message": "缺少expired或bucketName"}
            else:
                sign = Auth()
                sign = sign.appSign(expired=expired, bucketName=bucketName)
                return {"code": 0, "message": "成功", "data": sign}

        elif sign_type == "appSign_once":
            path = request.GET.get("path", None)
            bucketName = request.GET.get("bucketName", None)
            if path or bucketName is None:
                return {"code": 10001,"message": "缺少path或bucketName"}
            else:
                sign = Auth()
                sign = sign.appSign_once(path, bucketName)
                return {"code": 0, "message": "成功", "data": sign}

        else:
            return {"code": 10001, "message": "未指定签名方式"}
    except Exception as e:
        return {"code": -1, "message": "内部错误reason：" + str(e)}
