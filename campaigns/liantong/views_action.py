# -*- coding: utf-8 -*-
import math, datetime, pytz, random
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.liantong import models, config, const
from campaigns.foundation import wechat_api
from campaigns.liantong.applet import decorators
from campaigns.liantong.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos
from django.utils import timezone
from collections import Counter
from campaigns.liantong.applet.Tcos import Auth
from campaigns.liantong.applet.getLocation import txLocations


@decorators.action_render
def getyestExcel(request):
    nowday = datetime.date.today()
    l1 = []
    urlList = ['/lt/mobile/self.html', '/lt/mobile/ljl.html', '/lt/mobile/IndexNew.html', '/lt/mobile/boruina.html', '/lt/mobile/ddbb.html', '/lt/mobile/index.html',
               '/lt/mobile/lingjuli.html', '/lt/mobile/lizhi.html', '/lt/mobile/xiandai.html', '/lt/mobile/share.html', '/lt/mobile/nanjing', '/lt/mobile/suzhou',
               '/lt/mobile/wuxi', '/lt/mobile/changzhou', '/lt/mobile/zhengjiang',
               '/lt/mobile/nantong', '/lt/mobile/taizhou', '/lt/mobile/yangzhou', '/lt/mobile/yancheng'
               , '/lt/mobile/huaian', '/lt/mobile/suqian', '/lt/mobile/xuzhou', '/lt/mobile/lianyungang']
    for i in urlList:
        count = 0
        while True:
            if str(nowday - datetime.timedelta(days=count)) == "2016-11-05":
                break
            else:
                d1 = {}
                weekday = nowday - datetime.timedelta(days=count)
                d1['date'] = str(weekday)
                d1['url'] = i.split("/")[3]
                d1['当日上传总数'] = models.Work.objects.filter(creationTime__gte=weekday, creationTime__lt=weekday + datetime.timedelta(days=1)).all().count()
                d1['pv'] = models.PageView.objects.filter(creationTime=weekday, url=i).all().count()
                d1['uv'] = models.UniqueVisitor.objects.filter(creationTime=weekday, url=i).all().count()
                l1.append(d1)
                count += 1
    excel = decorators.exportExcel(request, "联通pvuv", l1)
    return excel


# 管理员登录
@decorators.action_render
def AdminLogIn(request):
    username = request.POST['username']
    passwd = request.POST['passwd']
    usrinfo = models.AdminUser.objects.filter(username=username).first()
    if usrinfo is not None:
        if passwd == usrinfo.userpasswd:
            request.session['usrname'] = username
            return {FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: "登陆成功"}
        else:
            return {FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: "密码错误"}
    else:
        return {FoundationConst.RN_RCODE: 2, FoundationConst.RN_RMSG: "用户名错误"}

@decorators.action_render
def changeStatus(request):
    try:
        workId = request.POST['id']
        changeUs = request.POST['status']
        models.Work.objects.filter(id=workId).update(status=changeUs)
        return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}



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
        url = request.POST['imageurl']
        phone = request.POST['phone']
        name = request.POST['name']
        city = request.POST['city']
        district = request.POST['district']
        addrinfo = request.POST['addrinfo']
        network = request.POST['network']
        l1 = [130, 131, 132, 155, 156, 185, 186, 175, 176]

        if int(phone[0: 3]) not in l1:
            return {"result_code": 2, "result_msg": "error phone number"}
        else:
            models.Work.objects.create(
                imageurl=url,
                phone=phone,
                name=name,
                city=city,
                district=district,
                addrinfo=addrinfo,
                network=network
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
            d1['id'] = i.id
            d1['图片地址'] = str(i.imageurl)
            d1['手机号'] = i.phone
            d1['姓名'] = i.name
            d1['城市'] = i.city
            d1['创建时间'] = str(i.creationTime)
            d1['区/县'] = i.district
            d1['详细地址'] = i.addrinfo
            d1['网络信息'] = i.network
            if i.status == 10:
                STATUS = "正常"
            else:
                STATUS = "封禁"
            d1['状态'] = STATUS
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
        total_count = models.Work.objects.all().count()
        locaData = models.Work.objects.all().order_by('-id')[start: end]
        l1 = []
        for i in locaData:
            d1 = {}
            d1['id'] = i.id
            d1['imageurl'] = str(i.imageurl)
            d1['phone'] = i.phone
            d1['creatime'] = str(i.creationTime)
            d1['name'] = i.name
            d1['city'] = i.city
            d1['district'] = i.district
            d1['addrinfo'] = i.addrinfo
            d1['network'] = i.network
            d1['status'] = i.status
            l1.append(d1)
        return {"result_code": 0, "result_msg": None, "pv": pv, "uv": uv, "data": l1, "total_count": total_count}
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


@decorators.action_render
def checkUp(request):
    Phone = request.POST['phone']

    info = models.Work.objects.filter(phone=Phone).first()
    if info is not None:
        return {"result_code": 0, "isUP": 1, "result_msg": None}
    else:
        return {"result_code": 0, "isUP": 0, "result_msg": None}



@decorators.action_render
def ltUpload(request):
    try:
        name = request.POST['name']
        phone = request.POST['phone']
        usrinfo = models.ltworkSec.objects.filter(phone=phone).first()
        if usrinfo is not None:
            return {"result_code": 1, "result_msg": "已上传过"}
        else:
            l1 = [130, 131, 132, 155, 156, 185, 186, 175, 176]
            if int(phone[0: 3]) in l1:
                isLT = 0
            else:
                isLT = 1
            work = models.ltworkSec.objects.create(
                name=name,
                phone=phone,
                isLT=isLT
            )
            return {'result_code': 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


import uuid
@decorators.action_render
def fakedata(request):
    while True:
        url = uuid.uuid4().hex
        phone = "123123123123"
        name = uuid.uuid4().hex[0: 3]
        city = uuid.uuid4().hex[4: 9]
        district = uuid.uuid4().hex[0: 9]
        addrinfo = uuid.uuid4().hex[5: 8]
        network = uuid.uuid4().hex[3:8]
        models.Work.objects.create(
            imageurl=url,
            phone=phone,
            name=name,
            city=city,
            district=district,
            addrinfo=addrinfo,
            network=network
        )
    return {"result_code": "0000"}



@decorators.action_render
def userInfo(request):
    phoneNum = request.POST['phone']
    name = request.POST['name']
    checkNum = models.usrInfo.objects.filter(phone=phoneNum).first()
    if checkNum is not None:
        return {"result_code": 1, "result_msg": "该号码已注册"}
    else:
        models.usrInfo.objects.create(name=name, phone=phoneNum)
        return {"result_code": 0, "result_msg": "success"}