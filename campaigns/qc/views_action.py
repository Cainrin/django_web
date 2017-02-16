# -*- coding: utf-8 -*-
import math, datetime, pytz, random
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.qc import models, config, const
from campaigns.foundation import wechat_api
from campaigns.qc.applet import decorators
from campaigns.qc.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos
from django.utils import timezone
from collections import Counter
from campaigns.qc.applet.Tcos import Auth
from campaigns.qc.applet.getLocation import txLocations




@decorators.action_render
def get_sign_package(request):
    try:
        url = request.POST['url']
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    sign_package = wechat_api.WechatApi().get_sign_package(url)
    return sign_package





@decorators.action_render
def uploadPage(request):
    try:
        sex = int(request.POST['sex'])
        phone = request.POST['phone']
        name = request.POST['name']
        city = request.POST['city']
        district = request.POST['district']
        distributor = request.POST['distributor']
        carType = request.POST['carType']
        models.Work.objects.create(
            sex=sex,
            phone=phone,
            name=name,
            city=city,
            district=district,
            distributor=distributor,
            carType=carType
        )
        return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}



@decorators.action_render
def getExcel(request):
    try:
        locaData = models.Work.objects.all().order_by('id')
        page_Count = request.GET.get("pageCount", None)
        page, count = page_Count.split(",")[0], page_Count.split(",")[1]
        l1 = []
        for i in locaData[int(page): int(count)]:
            d1 = {}
            d1['sex'] = i.sex
            d1['phone'] = i.phone
            d1['name'] = i.name
            d1['city'] = i.city
            d1['creatime'] = str(i.creationTime)
            d1['district'] = i.district
            d1['distributor'] = i.distributor
            d1['carType'] = i.carType
            l1.append(d1)
        excel = decorators.exportExcel(request, '数据单', l1)
        return excel
    except Exception as e:
        return {"result_code": 1, "result_msg": e}





@decorators.action_render
def backadmin(request):
    try:
        now_page = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        pv = models.PageView.objects.all().count()
        uv = models.WXUser.objects.all().count()
        start = (now_page - 1 ) * page_rows
        end = start + page_rows
        totalCount = models.Work.objects.all().count()
        locaData = models.Work.objects.all()[start: end]
        l1 = []
        for i in locaData:
            d1 = {}
            d1['sex'] = i.sex
            d1['phone'] = i.phone
            d1['name'] = i.name
            d1['city'] = i.city
            d1['creatime'] = str(i.creationTime)
            d1['district'] = i.district
            d1['distributor'] = i.distributor
            d1['carType'] = i.carType
            l1.append(d1)
        return {"result_code": 0, "result_msg": None, "pv": pv, "uv": uv, "data": l1, "total_count": totalCount}
    except Exception as e:
        return {"result_code": 1, "result_msg": e}






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



@decorators.action_render
def getLocation(request):
    location = request.GET['location']
    a = txLocations(location).getLocat()
    if a['status'] == 0:
        return str(a['result']['address_component']).replace('u\'', '\'').decode("unicode-escape") + a['result']['address']
    else:
        return a['message']

