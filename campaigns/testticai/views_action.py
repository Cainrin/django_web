# -*- coding: utf-8 -*-
import datetime
import json
import pytz
import time
from django.utils import timezone
from campaigns.foundation.applet import utils
from campaigns.foundation.const import DisplayConst
from campaigns.testticai import models, config, const, wechat_api
from campaigns.testticai.applet.uitls import save_work_image
from campaigns.testticai.applet import decorators
from campaigns.testticai.applet.Tcos import Auth
from django.core.cache import cache
import requests






#主kv
@decorators.action_render
def Main(request):
    try:
        activeinfo = models.walkCount.objects.all()
        count = 0
        Pcount = 0
        for i in activeinfo:
            if int(i.change) > 0:
                count += int(i.change)
            else:
                count += int(i.walk)
        TotalMon = round(float(count) / 2000, 2)

        return {"count": count, "money": TotalMon, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}



# 步数上传
@decorators.action_render
def update(request):
    try:
        now = timezone.now()
        now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.utc)
        walkInfo = models.walkCount.objects.filter(openid=request.session.get("wxUser")).filter(creaTime__gte=now).first()
        if walkInfo is not None:
            return {"result_code": 1, "result_msg": "您今日已上传过"}
        else:
            openid = request.session.get("wxUser")
            wxuser = models.walkCount.objects.filter(openid=openid).first()
            image = request.POST['img'].encode("utf-8")
            count = request.POST['count']
            usrprice = models.UsrPhoneCall.objects.filter(openid=openid).first()
            if usrprice is None:
                usrprice = models.UsrPhoneCall.objects.create(
                    openid=openid
                )
                usrdate = models.walkCount.objects.create(
                    # openid=request.session.get('wxUser'),
                    openid=openid,
                    image=image,
                    walk=count,
                    money=round(float(count) / 2000, 2),
                    info=usrprice,
                    priCode=None,
                )
                return {"result_code": 0, "result_msg": None, "first": False, "id": usrdate.id, 'walk': count, "money": round(float(count) / 2000, 2)}
            else:
                usrdate = models.walkCount.objects.create(
                    openid=openid,
                    image=image,
                    walk=count,
                    money=round(float(count) / 2000, 2),
                    info=usrprice,
                    priCode=None,
                )
                return {"result_code": 0, "result_msg": None, "first": False, "id": usrdate.id, 'walk': count, "money": round(float(count) / 2000, 2)}
    except Exception as e:
        return {'result_code': -1, "result_msg": str(e)}



@decorators.action_render
def suchAll(request):
    openid = request.GET['openid']
    if openid == request.session.get("wxUser"):
        return {"isSelf": 0}
    else:
        mywork = models.walkCount.objects.filter(openid=openid).all()
        count = 0
        Pcount = 0
        for i in mywork:
            if int(i.change) > 0:
                count += int(i.change)
            else:
                count += int(i.walk)
        TotalMon = round(float(count) / 2000, 2)
    return {"count": count, "money": TotalMon, "result_code": 0, "result_msg": None, "isSelf": 1}




@decorators.action_render
def firstUp(request):
    openid = request.session.get("wxUser")
    walkInfo = models.walkCount.objects.filter(openid=openid).first()

    if walkInfo is None:
        return {"result_code": 0, "result_msg": None}
    else:
        tel = "".join(str(walkInfo.info.usractive).split(" ")[1])
        name = "".join(str(walkInfo.info.usractive).split(" ")[3])
        return {"result_code": 1, "result_msg": None, "phone": tel, "name": name}


#监测当天上传
@decorators.action_render
def checktoday(request):
    now = timezone.now()
    now = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.utc)
    walkInfo = models.walkCount.objects.filter(openid=request.session.get("wxUser")).filter(
        creaTime__gte=now).first()
    if walkInfo is not None:
        walk = None
        if walkInfo.change != "0":
            if int(walkInfo.change) == 0:
                walk = 0
            else:
                walk = walkInfo.change
        else:
            walk = walkInfo.walk
        return {"result_code": 1, "result_msg": "已上传过", "walk": walk, "id": walkInfo.openid}
    else:
        return {"result_code": 0, "result_msg": "为上传"}




# 查询个人不熟
@decorators.action_render
def fetchwork(request):
    try:
        # openid = request.session.get("wxUser")
        openid = request.session.get("wxUser")
        mywork = models.walkCount.objects.filter(openid=openid).all()
        count = 0
        Pcount = 0
        for i in mywork:
            if int(i.change) > 0:
                count += int(i.change)
            else:
                count += int(i.walk)
        TotalMon = round(float(count) / 2000, 2)
        return {"count": count, "money": TotalMon, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}



# 总排名以及个人名次查询
@decorators.action_render
def workcount(request):
    try:
        openid = request.session.get("wxUser")
        myusr = models.WXUser.objects.filter(openid=openid).first()
        wxusr = models.WXUser.objects.all()
        l1 = []
        l2 = []
        l4 = []
        for i in wxusr:
            d1 = {}
            activeUser = models.walkCount.objects.filter(openid=i.openid).all()
            count = 0
            for _i in activeUser:
                if int(_i.change) > 0:
                    count += int(_i.change)
                    d2 = {}
                    d2['count'] = _i.walk
                    d2['time'] = _i.creaTime
                    d2['change'] = _i.change
                    l4.append(d2)
                else:
                    count += int(_i.walk)
            d1['count'] = count
            d1['user'] = i.id
            l1.append(d1)
        l2 = sorted(l1, key=lambda x: x["count"], reverse=True)
        rank = 1
        _data = None
        for obj in l2:
            if obj['user'] == myusr.id:
                _data = obj['count']
                break
            else:
                rank += 1
        l3 = []
        mydata = models.walkCount.objects.filter(openid=openid).all()
        for DATA in mydata:
            d1 = {}
            d1['count'] = DATA.walk
            d1['time'] = str(DATA.creaTime)
            l3.append(d1)
        l3 = sorted(l3, key=lambda x: x['time'], reverse=True)
        return {"rank_count": l2[0: 19], "result_code": 0, "result_msg": None, "my_count": _data, "my_rank": rank, "my_data": l3, "change_list": l4, "user": myusr.id}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


# 查询用户奖品提醒
@decorators.action_render
def PriCount(request):
    try:
        openId = request.session.get("wxUser")
        if request.session.get("price"):
            if models.walkCount.objects.filter(openid=openId).filter(priCode__isnull=False).count() == 0:
                return {"price_new": 0, "result_code": 0, "result_msg": None}
            else:
                count = models.walkCount.objects.filter(openid=openId).filter(priCode__isnull=False).count() - request.session.get("price")
        else:
            count = models.walkCount.objects.filter(openid=openId).filter(priCode__isnull=False).count()
        return {"price_new": count, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": 0, "result_msg": e}


# 查询日排周排名
@decorators.action_render
def myDonate(request):
    try:
        openid = request.session.get("wxUser")
        myId = models.WXUser.objects.filter(openid=openid).first()
        weekCount = 1
        firstWeek = models.hitprize.objects.filter(countType=0).all()
        L1 = []
        for i in firstWeek:
            d1 = {}
            count = 1
            myWalk = 0
            d1['weekCount'] = i.weekMacht
            d1['isend'] = i.isSend
            List1 = json.loads(i.usrList)['data']
            for j in List1:
                if j['user'] == myId.id:
                    myWalk = j['walk']
                    break
                else:
                    count += 1
            if myWalk == 0:
                d1['rank'] = None
                d1['myWalk'] = 0
            else:
                d1['rank'] = count
                d1['myWalk'] = myWalk
            L1.append(d1)
        nowDay = datetime.date.today()
        weekDayd = nowDay - datetime.timedelta(days=1)
        Dcount = models.hitprize.objects.filter(countType=1).filter(isSend=0).filter(creatime__gte=nowDay).first()
        dayCount = models.hitprize.objects.filter(countType=1).filter(isSend=0).all().order_by("-creatime")
        if dayCount is not None:
            l1 = []
            for j in dayCount:
                d1 = {}
                creaTime = 0
                rank = 0
                walk = 0
                info = None
                valueList = json.loads(j.usrList)['data']
                for i in valueList:
                    if i['user'] == myId.id:
                        if i is not None:
                            creaTime = i['creatime']
                            rank = i['rank']
                            walk = i['walk']
                            if i.has_key("info"):
                                info = i['info']
                        break
                d1['weekMatch'] = j.weekMacht
                d1['creatime'] = creaTime
                d1['rank'] = rank
                d1['walk'] = walk
                d1['info'] = info
                l1.append(d1)
            if Dcount is not None:
                myData = models.walkCount.objects.filter(creaTime__gte=nowDay).filter(openid=openid).all()
            else:
                myData = models.walkCount.objects.filter(creaTime__gte=weekDayd).filter(openid=openid).all()
            l2 = []
            if myData is not None:
                for M in myData:
                    d2 = {}
                    d2['user'] = myId.id
                    if M.change != "0":
                        if int(M.change) == 0:
                            d2['walk'] = 0
                        else:
                            d2['walk'] = M.change
                    else:
                        d2['walk'] = M.walk
                    d2['id'] = M.id
                    d2['creatime'] = str(M.creaTime).split(" ")[0] + " " + str(M.creaTime).split(" ")[1].split(".")[0]
                    l2.append(d2)
        else:
            l1 = []
            myData = models.walkCount.objects.filter(creaTime__gte=weekDayd).filter(openid=openid).all()
            l2 = []
            for i in myData:
                if i is None:
                    continue
                else:
                    d2 = {}
                    d2['user'] = myId.id
                    if i.change != "0":
                        if int(i.change) == 0:
                            d2['walk'] = 0
                        else:
                            d2['walk'] = int(i.change)
                    else:
                        d2['walk'] = int(i.walk)
                    d2['id'] = i.id
                    d2['creatime'] = str(i.creaTime).split(" ")[0] + " " + str(i.creaTime).split(" ")[1].split(".")[0]
                    l2.append(d2)
        return {"week": L1, "day": l1, "result_code": 0, "result_msg": None, "no_check": l2}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}




# 个人奖品查询
@decorators.action_render
def fetchprice(request):
    try:
        openid = request.session.get("wxUser")
        usrdate = models.walkCount.objects.filter(openid=openid).filter(priCode__isnull=False).all().order_by("creaTime")
        request.session['price'] = usrdate.count()
        l1 = []
        count = 6
        for i in usrdate:
            d1 = {}
            price = models.qrcount.objects.get(id=i.priCode)
            d1['price'] = price.code
            d1['passwd'] = price.passwd
            d1['img'] = price.qrimg.url
            d1['endtime'] = price.endtime
            d1['time'] = str(i.creaTime)
            d1['id'] = i.id
            d1['usrname'] = i.info.usrprizes
            l1.append(d1)
            count += 1
        return {"priceinfo": l1, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"priceinfo": None, "result_code": -1, "result_msg": e}



# 个人信息补全
@decorators.action_render
def signup(request):
    try:
        usrinfo = request.POST['usrinfo']
        # openid = request.session.get("wxUser")
        openid = request.session.get("wxUser")
        USER = models.walkCount.objects.filter(openid=openid).all()
        DT = models.UsrPhoneCall.objects.filter(openid=openid)
        if DT is None:
            WT = models.UsrPhoneCall.objects.create(
                openid=openid,
                usrsignup=usrinfo,
                signuptime=time.time()
            )
            l1 = []
            for i in USER:
                l1.append(i.id)
            for i in l1:
                models.walkCount.objects.filter(id=i).update(info=WT)
            return {"result_code": 0, "result_msg": None}
        else:
            DT.update(usrsignup=usrinfo, signuptime=time.time())
            l1 = []
            for i in USER:
                l1.append(i.id)
            for i in l1:
                models.walkCount.objects.filter(id=i).update(info=DT[0])
            return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


@decorators.action_render
def usrprices(request):
    try:
        usrinfo = request.GET['usrinfo']
        # openid = request.session.get('wxUser')
        openid = request.session.get("wxUser")
        USER = models.walkCount.objects.filter(openid=openid).all()
        DT = models.UsrPhoneCall.objects.filter(openid=openid)
        if DT is None:
            WT = models.UsrPhoneCall.objects.create(
                openid=openid,
                usrprizes=usrinfo,
                prizetime=time.time()
            )
            l1 = []
            for i in USER:
                l1.append(i.id)
            for i in l1:
                models.walkCount.objects.filter(id=i).update(info=WT)
            return {"result_code": 0, "result_msg": None}
        else:
            DT.update(usrprizes=usrinfo, prizetime=time.time())
            l1 = []
            for i in USER:
                l1.append(i.id)
            for i in l1:
                models.walkCount.objects.filter(id=i).update(info=DT.first())
            return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}



@decorators.action_render
def activeuser(request):
    try:
        usrinfo = request.POST['usrinfo']
        # openid = request.session.get('wxUser')
        openid = request.session.get("wxUser")
        USER = models.walkCount.objects.filter(openid=openid).all()
        DT = models.UsrPhoneCall.objects.filter(openid=openid)
        if DT is None:
            WT = models.UsrPhoneCall.objects.create(
                openid=openid,
                usractive=usrinfo,
            )
            l1 = []
            for i in USER:
                l1.append(i.id)
            for i in l1:
                models.walkCount.objects.filter(id=i).update(info=WT)
            return {"result_code": 0, "result_msg": None}
        else:
            DT.update(usractive=usrinfo)
            l1 = []
            for i in USER:
                l1.append(i.id)
            for i in l1:
                models.walkCount.objects.filter(id=i).update(info=DT.first())
            return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


# 周排行
@decorators.action_render
def weekCount(request):
   try:
        now_page = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (now_page - 1) * page_rows
        end = start + page_rows
        now = timezone.datetime.today()
        nowday = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        weekDayd = nowday - datetime.timedelta(days=1)
        matWek = str(datetime.date.today() - datetime.date.fromtimestamp(config.WorkConfig.starTime))
        if matWek == "0:00:00":
            matchWek = 0
        else:
            matchWek = int(matWek.split(" ")[0])
        if 0 <= matchWek < 7:
            weekCount = 1

        elif 7 <= matchWek < 14:
            weekCount = 2
            matchWek -= 7
        else:
            weekCount = 3
            matchWek -= 14
        weekCount = models.hitprize.objects.filter(creatime__gte=weekDayd, countType=0, weekMacht=weekCount).first()
        if weekCount is None:
            return {"result_code": 1, "result_msg": "数据正在审核"}
        else:
            openid = request.session.get("wxUser")
            dataList = json.loads(weekCount.usrList)['data']
            ID = models.WXUser.objects.filter(openid=openid).first().id
            count = 1
            d2 = {}
            for i in dataList:
                if ID == i['user']:
                    d2["user"] = i['user']
                    d2['walk'] = i['walk']
                    d2['info'] = i['info']
                    break
                else:
                    count += 1
            if ID not in [ i['user'] for i in dataList ]:
                count = None
            if ID in [ i['user'] for i in dataList[0: 9] ]:
                isWrite = models.UsrPhoneCall.objects.filter(openid=openid).first()
                if isWrite.usrprizes is None:
                    infoSend = 0
                else:
                    infoSend = 1
            else:
                infoSend = 1
            dataList = sorted(dataList, key=lambda x: x["walk"], reverse=True)
            return {"result_code": 0, "result_msg": None, "isUser": infoSend, "walkCount": dataList[start: end], "myCount": d2, "total_count": len(dataList),
                    "my_rank": count, "now_week": weekCount.weekMacht, "isSend": weekCount.isSend}
   except Exception as e:
       return {"result_code": -1, "result_msg": e}




# 验证码查询
@decorators.action_render
def fetchCode(request):
    try:
        priceId = request.POST['id']
        price = models.qrcount.objects.filter(id=priceId).first()
        models.qrcount.objects.filter(id=priceId).update(time.time())
        return {"qrcode": price.qrimg.url, "endtime": price.endtime}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}



@decorators.action_render
def get_sign_package(request):
    try:
        url = request.POST['url']
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    sign_package = wechat_api.WechatApi().get_sign_package(url)
    return sign_package


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