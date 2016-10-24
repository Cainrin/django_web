# -*- coding: utf-8 -*-
# 后台控制接口
import time, datetime, pytz, config, uuid
import random, json, copy
from django.utils import timezone
from campaigns.foundation.const import FoundationConst
from campaigns.testticai import models, const
from campaigns.testticai.applet.uitls import save_work_file
from campaigns.testticai.applet import decorators, QRCode, walkExcel, makeName



# 奖卷信息查询
@decorators.action_render
def priceInfo(request):
    try:
        nowpage = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (nowpage - 1) * page_rows
        end = start + page_rows
        startime = timezone.datetime.strptime(request.GET['startime'], "%Y-%m-%d").date()
        endtime = timezone.datetime.strptime(request.GET['endtime'], "%Y-%m-%d").date()
        total_count = models.walkCount.objects.filter(priCode__isnull=False).filter(creaTime__lte=endtime).filter(creaTime__gte=startime).all().count()
        hitPrizeinfo = models.walkCount.objects.filter(priCode__isnull=False).filter(creaTime__lte=endtime).filter(creaTime__gte=startime).all()
        l1 = []
        for i in hitPrizeinfo:
            d1 = {}
            wxObj = models.WXUser.objects.filter(openid=i.openid).first()
            d1['id'] = wxObj.id
            usrphone = models.UsrPhoneCall.objects.get(openid=wxObj.openid)
            d1['info'] = "".join(str(usrphone.usractive).split(" ")[1])
            inFo = models.qrcount.objects.filter(id=i.priCode).first()
            d1['pricode'] = str(inFo.code)
            d1['endtime'] = inFo.endtime
            d1['sendTime'] = inFo.sendTime
            l1.append(d1)
        if request.GET['excel'] == '1':
            excel = decorators.exportExcel(request, name='pricode', dict1=l1)
            return excel
        else:
            return {"list": l1[start: end], "total_count": total_count, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": 1, "result_msg": e}


# 查看已有蒋娟文件
@decorators.action_render
def suchPrifile(request):
    try:
        l1 = []
        fileLoad = models.addCode.objects.all()
        for i in fileLoad:
            d1 = {}
            d1['isSend'] = i.issuccess
            d1['id'] = i.id
            d1['creatime'] = str(i.creatime)
            l1.append(d1)
        return {"data": l1}
    except Exception as e:
        return {"result_msg": e}



# 查看中奖用户
@decorators.action_render
def fetchPriz(request):
    try:
        Type = request.GET['type']
        nowpage = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (nowpage - 1) * page_rows
        end = start + page_rows
        if Type == "week":
            inFo = models.hitprize.objects.filter(isSend=1, countType=0).all()
            if inFo:
                l1 = []
                for d in inFo[start: end]:
                    d1 = {}
                    openID = models.WXUser.objects.filter(openid=d.usr).first()
                    d1['id'] = openID.id
                    d1['walk'] = d.walk
                    d1['weekCount'] = d.weekMacht
                    l1.append(d1)
                if request.GET['excel'] == 1:
                    l1 = []
                    for d in inFo:
                        d1 = {}
                        openID = models.WXUser.objects.filter(openid=d.usr).first()
                        d1['id'] = openID.id
                        d1['walk'] = d.walk
                        d1['weekCount'] = d.weekMacht
                        l1.append(d1)
                    excel = decorators.exportExcel(request, name='pricode', dict1=l1)
                    return excel
                else:
                    return {"countList": l1, "result_code": 0, "result_msg": None, "total_count": inFo.count()}
        else:
            return {"result_code": 2, "result_msg": "暂无数据"}
        if Type == "day":
            inFo = models.hitprize.objects.filter(isSend=1, countType=1).all()
            if inFo:
                l1 = []
                for d in inFo[start: end]:
                    d1 = {}
                    d1['id'] = models.WXUser.objects.get(openid=models.walkCount.objects.get(id=d.usr).openid).id
                    d1['walk'] = d.walk
                    d1['weekCount'] = d.weekMacht
                    l1.append(d1)
                if request.GET['excel'] == 1:
                    l1 = []
                    for d in inFo:
                        d1 = {}
                        d1['id'] = models.WXUser.objects.get(openid=models.walkCount.objects.get(id=d.usr).openid).id
                        d1['walk'] = d.walk
                        d1['weekCount'] = d.weekMacht
                        l1.append(d1)
                    excel = decorators.exportExcel(request, name='pricode', dict1=l1)
                    return excel
                else:
                    return {"countList": l1,"total_count": inFo.count(), "result_code": 0, "result_msg": None}
            else:
                return {"result_code": 2, "result_msg": "暂无数据"}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}



# 上传奖券文件
@decorators.action_render
def upload(request):
    try:
        filename = save_work_file((request.FILES[const.ViewConst.RN_WORK_IMAGE]))
        file = codefile = models.addCode.objects.create(
            File=filename
        )
        return {'result_code': 0, "result_msg": None, 'id': file.id}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


# 生成奖券以及二维码
@decorators.action_render
def startAdd(request):
    try:
        addID = request.GET['id']
        fileName = models.addCode.objects.filter(id=addID).filter(issuccess=1).first()
        if fileName is not None:
            fileUrl = str(fileName.File).strip("./")
            start_add = QRCode.addQRCODE(fileUrl)
            runDraw = start_add.startDraw()
            if runDraw == "success":
                models.addCode.objects.filter(id=addID).update(issuccess=0)
                return {"result_code": 0, "result_msg": 'success'}
            else:
                return {"result_code": -1, "result_msg": runDraw}
        else:
            return {"result_code": 1, "result_msg": "重复操作"}
    except Exception as e:
        return {"result_code": -2, "result_msg": e}


# 查询当前奖品池
@decorators.action_render
def fetchCode(request):
    try:
        nowpage = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (nowpage - 1) * page_rows
        end = start + page_rows
        l1 = []
        total_count = models.qrcount.objects.all().count()
        for i in models.qrcount.objects.all()[start: end]:
            d1 = {}
            d1["code"] = i.code
            d1['passwd'] = i.passwd
            d1['img'] = str(i.qrimg)
            d1['startime'] = i.startime
            d1['endtime'] = i.endtime
            d1['isend'] = i.isend
            d1['sendTime'] = i.sendTime
            l1.append(d1)
        return {"code_list": l1, "total_count": total_count, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


@decorators.action_render
def dayPuv(request):
    try:
        starTime = request.GET['startime']
        endtime = request.GET['endtime']
        pvCount = models.PageView.objects.filter(creationTime__gte=starTime).filter(creationTime__lte=endtime).count()
        uvCount = models.UniqueVisitor.objects.filter(creationTime__gte=starTime).filter(creationTime__lte=endtime).count()
        return {"pv": pvCount, "uv": uvCount, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}



# pv uv
@decorators.action_render
def _PUv(request):
    try:
        Pcount = models.CountPUV.objects.filter(id=1)[0]
        _PV = int(Pcount.pv) + int(Pcount.addpv)
        _UV = int(Pcount.uv) + int(Pcount.adduv)
        return {"pv": _PV, "uv": _UV, FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {"pv": None, "uv": None, FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: e}



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





# 活动数据
@decorators.action_render
def ActiveData(request):
    try:
        nowpage = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (nowpage - 1) * page_rows
        end = start + page_rows
        total_count = models.walkCount.objects.all().count()
        statime = request.GET['timestart']
        endtime = request.GET['timend']
        if request.GET['type'] == "1":
            activedata = models.walkCount.objects.all()
            l1 = []
            for i in activedata:
                d2 = {}
                d2['id'] = models.WXUser.objects.filter(openid=i.openid).first().id
                d2['cid'] = i.id
                d2['picture'] = str(i.image)
                d2['count'] = i.walk
                d2['change'] = i.change
                d2['money'] = i.money
                d2['pricesname'] = i.priCode
                d2['update'] = str(i.creaTime)
                d2['phonecall'] = i.info.usractive
                l1.append(d2)
            excel = decorators.exportExcel(request, name="活动数据", dict1=l1)
            return excel
        elif request.GET['suchchoice'] == "time":
            total_count = models.walkCount.objects.all().filter(creaTime__lte=endtime).filter(
                creaTime__gte=statime).order_by("creaTime").count()
            activedata = models.walkCount.objects.all().filter(creaTime__lte=endtime).filter(creaTime__gte=statime).order_by("creaTime")[start: end]
            l1 = []
            for i in activedata:
                if i.image is None:
                    continue
                else:
                    d1 = {}
                    d1['id'] =  models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['Cid'] = i.id
                    d1['picture'] = str(i.image)
                    d1['count'] = i.walk
                    d1['change'] = i.change
                    d1['money'] = i.money
                    d1['pricesname'] = i.priCode
                    d1['update'] = str(i.creaTime)
                    d1['phonecall'] = i.info.usractive
                    l1.append(d1)
            return {"acivedata": l1, "total_count": total_count, FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: None}
        else:
            total_count = models.walkCount.objects.all().filter(creaTime__lte=endtime).filter(
                creaTime__gte=statime).order_by("creaTime").count()
            activedata = models.walkCount.objects.all().filter(creaTime__lte=endtime).filter(creaTime__gte=statime).order_by("-change")[start: end]
            l1 = []
            for i in activedata:
                d1 = {}
                d1['id'] =  models.WXUser.objects.filter(openid=i.openid).first().id
                d1['Cid'] = i.id
                d1['picture'] = str(i.image)
                d1['count'] = i.walk
                d1['change'] = i.change
                d1['money'] = i.money
                d1['pricesname'] = i.priCode
                d1['update'] = str(i.creaTime)
                d1['phonecall'] = i.info.usractive
                l1.append(d1)
            return {"acivedata": l1, "total_count": total_count, FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {"activedata": None, "total_count": None, FoundationConst.RN_RCODE: -1, FoundationConst.RN_RMSG: e}




# 用户数据
@decorators.action_render
def UserData(request):
    try:
        now_page = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (now_page - 1) * page_rows
        end = start + page_rows
        total_page = models.WXUser.objects.all().count()
        USRDATA = models.WXUser.objects.all()[start: end]
        l1 = []
        for i in USRDATA:
            userdata = models.walkCount.objects.filter(openid=i.openid).all()
            usercount = len(userdata.values_list())
            if userdata:
                count = 0
                Pcount = 0
                a = None
                for _i in userdata:
                    if int(_i.change) <= 0:
                        count += int(_i.walk)
                    else:
                        count += int(_i.change)

                d1 = {}
                usrinfo = models.UsrPhoneCall.objects.filter(openid=i.openid).first()
                if usrinfo is None:
                    d1['info'] = None
                else:
                    d1['info'] = "".join(str(usrinfo.usractive).split(" ")[1])
                d1['money'] = round(float(count) / 2000, 2) + Pcount
                d1['username'] = i.id
                d1['count'] = count
                d1['joincount'] = usercount
                l1.append(d1)
            else:
                d1 = {}
                d1['username'] = i.id
                d1['money'] = 0
                d1['count'] = 0
                d1['joincount'] = 0
                l1.append(d1)
        if request.GET['suchchoice'] == "time":
            l2 = sorted(l1, key=lambda x: x["joincount"], reverse=True)
        else:
            l2 = sorted(l1, key=lambda x: x["count"], reverse=True)
        if request.GET['type'] == "1":
            excel = decorators.exportExcel(request, "数据表", l2)
            return excel
        else:
            return {"userdata": l2, 'total_page': total_page, FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {"userdata": None, FoundationConst.RN_RCODE: -1, 'total_page': None, FoundationConst.RN_RMSG: str(e)}


# 实物奖品
@decorators.action_render
def SWPrices(request):
    try:
        Getype = request.GET['type']
        week = request.GET['week']
        now_page = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (now_page - 1) * page_rows
        end = start + page_rows
        swcount = models.hitprize.objects.filter(isSend=0).filter(weekMacht=int(week)).filter(countType=0).first()
        if swcount is None:
            return {"result_code": 1, "result_msg": "暂无数据"}
        if Getype == "1":
            dataCount = models.weekCount.objects.filter(weekMatch=week).order_by('-walk').all()
            l1 = []
            if dataCount.count() <= 50:
                for j in dataCount[start: end]:
                    d1 = {}
                    d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=j.openid)[0].usractive.split(" ")[1])
                    d1['user'] = models.WXUser.objects.filter(openid=j.openid).first().id
                    d1['rank'] = models.weekCount.objects.filter(walk__gt=j.walk).count() + 1
                    d1['walk'] = j.walk
                    d1['weekCount'] = j.weekMacht
                    l1.append(d1)
            else:
                for j in swcount[0: 49]:
                    d1 = {}
                    d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=j.openid)[0].usractive.split(" ")[1])
                    d1['user'] = models.WXUser.objects.filter(openid=j.openid).first().id
                    d1['rank'] = models.weekCount.objects.filter(walk__gt=j.walk).count() + 1
                    d1['walk'] = j.walk
                    d1['weekCount'] = j.weekMacht
                    l1.append(d1)
            excel = decorators.exportExcel(request, '实物奖品', l1)
            return excel
        else:
            l1 = []
            if swcount.count() <= 50:
                for j in swcount[start: end]:
                    d1 = {}
                    d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=j.openid)[0].usractive.split(" ")[1])
                    d1['user'] = models.WXUser.objects.filter(openid=j.openid).first().id
                    d1['rank'] = models.weekCount.objects.filter(walk__gt=j.walk).count() + 1
                    d1['walk'] = j.walk
                    d1['weekCount'] = j.weekMacht
                    l1.append(d1)
                else:
                    for j in swcount[0: 49]:
                        d1 = {}
                        d1['info'] = "".join(
                            models.UsrPhoneCall.objects.filter(openid=j.openid)[0].usractive.split(" ")[1])
                        d1['user'] = models.WXUser.objects.filter(openid=j.openid).first().id
                        d1['rank'] = models.weekCount.objects.filter(walk__gt=j.walk).count() + 1
                        d1['walk'] = j.walk
                        d1['weekCount'] = j.weekMacht
                        l1.append(d1)
            return {'swdata': l1[start: end], 'total_page': swcount.count(), FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {'swdata': None, FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: str(e)}


# 线下报名
@decorators.action_render
def SignUp(request):
    try:
        now_page = int(request.GET.get('now_page', None))
        page_rows = int(request.GET.get('page_rows', None))
        start = (now_page - 1) * page_rows
        end = start + page_rows
        timestart = request.GET.get('timestart', None)
        timend = request.GET.get('timend', None)
        if timestart is not None:
            timestart = float(time.mktime(time.strptime(timestart, '%Y-%m-%d')))
            timend = float(time.mktime(time.strptime(timend, '%Y-%m-%d')))
            total_count = models.UsrPhoneCall.objects.filter(signuptime__lte=timend).filter(signuptime__gte=timestart).all().count()
        offlinesign = models.UsrPhoneCall.objects.all()
        l1 = []
        for i in offlinesign:
            if i.usrsignup is None:
                continue
            d1 = {}
            d1['userid'] = i.id
            _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.signuptime))
            d1['updatetime'] = _time
            d1['phonecall'] = i.usrsignup
            l1.append(d1)
        Getype = request.GET['type']
        if Getype == "1":
            offlinesign = models.UsrPhoneCall.objects.all()
            l1 = []
            for i in offlinesign:
                if i.usrsignup is None:
                    continue
                d1 = {}
                d1['userid'] = i.id
                _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.signuptime))
                d1['updatetime'] = _time
                d1['phonecall'] = i.usrsignup
                l1.append(d1)
            excel = decorators.exportExcel(request, '线下报名', l1)
            return excel
        else:
            return {"signup": l1[start: end], 'total_count': len(l1), FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {'signup': None, 'total_count': None, FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: e}


# 活动数据搜寻
@decorators.action_render
def SuchActive(request):
    try:
        now_page = int(request.POST['now_page'])
        page_rows = int(request.POST['page_rows'])
        start = (now_page - 1) * page_rows
        end = start + page_rows
        usrid = request.POST.get("id", None)
        if usrid is not None:
            l1 = []
            timestart = request.POST['timestart']
            timend = request.POST['timend']
            openid = models.WXUser.objects.filter(id=usrid).first()
            total_count = models.walkCount.objects.filter(openid=openid.openid, creaTime__gte=timestart,
                                                          creaTime__lte=timend).all().count()

            if request.POST['type'] == "time" and request.POST.get("extype", None) != "1":
                userinfo = models.walkCount.objects.filter(openid=openid.openid, creaTime__gte=timestart,
                                                           creaTime__lte=timend).all().order_by('-creaTime')[start: end]
                for i in userinfo:
                    d1 = {}
                    d1['usrid'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['Cid'] = i.id
                    d1['picture'] = str(i.image)
                    d1['count'] = i.walk
                    d1['change'] = i.change
                    d1['money'] = i.money
                    d1['pricesname'] = i.priCode
                    d1['updatetime'] = str(i.creaTime)
                    d1['username'] = i.info.usractive
                    l1.append(d1)
                return {"suchdata": l1, 'total_count': total_count, FoundationConst.RN_RCODE: 0,
                        FoundationConst.RN_RMSG: None}
            elif request.POST.get('extype', None) == "1":
                userinfo = models.walkCount.objects.filter(openid=openid.openid, creaTime__gte=timestart,
                                                           creaTime__lte=timend).all()
                for i in userinfo:
                    d1 = {}
                    d1['usrid'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['Cid'] = i.id
                    d1['picture'] = str(i.image)
                    d1['count'] = i.walk
                    d1['change'] = i.change
                    d1['money'] = i.money
                    d1['pricesname'] = i.priCode
                    d1['updatetime'] = str(i.creaTime)
                    d1['username'] = i.info.usractive
                    l1.append(d1)
                excel = decorators.exportExcel(request, name='活动数据', dict1=l1)
                return excel
            else:

                l1 = []
                userinfo = models.walkCount.objects.filter(openid=openid.openid, creaTime__gte=timestart,
                                                           creaTime__lte=timend).all().order_by('-change')[start: end]
                total_count = models.walkCount.objects.filter(openid=openid.openid, creaTime__gte=timestart,
                                                           creaTime__lte=timend).all().count()
                for i in userinfo:
                    d1 = {}
                    d1['usrid'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['Cid'] = i.id
                    d1['picture'] = str(i.image)
                    d1['count'] = i.walk
                    d1['change'] = i.change
                    d1['money'] = i.money
                    d1['pricesname'] = i.priCode
                    d1['updatetime'] = str(i.creaTime)
                    d1['username'] = i.info.usractive
                    l1.append(d1)

                return {"suchdata": l1, 'total_count': total_count, FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
        else:
            l1 = []
            timestart = request.POST['timestart']
            timend = request.POST['timend']
            total_count = models.walkCount.objects.filter(creaTime__gte=timestart,
                                                          creaTime__lte=timend).all().count()

            if request.POST['type'] == 'time' and request.POST['extype'] == None:
                userinfo = models.walkCount.objects.filter(creaTime__gte=timestart,
                                                           creaTime__lte=timend).all().order_by(
                    '-creaTime')[start: end]
                for i in userinfo:
                    d1 = {}
                    d1['usrid'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['Cid'] = i.id
                    d1['picture'] = str(i.image)
                    d1['count'] = i.walk
                    d1['change'] = i.change
                    d1['money'] = i.money
                    d1['pricesname'] = i.priCode
                    d1['updatetime'] = str(i.creaTime)
                    d1['username'] = i.info.usractive
                    l1.append(d1)
                return {"suchdata": l1, 'total_count': total_count, FoundationConst.RN_RCODE: 0,
                        FoundationConst.RN_RMSG: None}
            elif request.POST['extype'] == "1":
                userinfo = models.walkCount.objects.filter(creaTime__gte=timestart,
                                                           creaTime__lte=timend).all()
                for i in userinfo:
                    d1 = {}
                    d1['usrid'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['Cid'] = i.id
                    d1['picture'] = str(i.image)
                    d1['count'] = i.walk
                    d1['change'] = i.change
                    d1['money'] = i.money
                    d1['pricesname'] = i.priCode
                    d1['updatetime'] = str(i.creaTime)
                    d1['username'] = i.info.usractive
                    l1.append(d1)
                excel = decorators.exportExcel(request, name='活动数据', dict1=l1)
                return excel
            else:
                userinfo = models.walkCount.objects.filter(creaTime__gte=timestart,
                                                            creaTime__lte=timend).all().order_by(
                    '-change')[start: end]
                for i in userinfo:
                    d1 = {}
                    d1['usrid'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['Cid'] = i.id
                    d1['picture'] = str(i.image)
                    d1['count'] = i.walk
                    d1['change'] = i.change
                    d1['money'] = i.money
                    d1['pricesname'] = i.priCode
                    d1['updatetime'] = str(i.creaTime)
                    d1['username'] = i.info.usractive
                    l1.append(d1)
                return {"suchdata": l1, 'total_count': total_count, FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {FoundationConst.RN_RCODE: -1, FoundationConst.RN_RMSG: e}



# 用户数据搜寻
@decorators.action_render
def SuchUser(request):
    try:
        now_page = int(request.POST['now_page'])
        page_rows = int(request.POST['page_rows'])
        start = (now_page - 1) * page_rows
        end = start + page_rows
        usrid = request.POST['id']
        d1 = {}
        openid = models.WXUser.objects.get(id=usrid)
        usrinfo = models.UsrPhoneCall.objects.get(openid=openid.openid)
        l1 = []
        total_count = models.walkCount.objects.filter(openid=openid.openid).all().count()
        if request.POST['suchchoice'] == "time":
            userdata = models.walkCount.objects.filter(openid=openid.openid).all().order_by('-creaTime')[start: end]
        else:
            userdata = models.walkCount.objects.filter(openid=openid.openid).all().order_by('-walk')[start: end]
        usercount = len(userdata.values_list())
        if userdata is not None:
            count = 0
            Pcount = 0
            a = None
            for _i in userdata:
                if _i.change is None:
                    count += int(_i.walk)
                else:
                    count += int(_i.change)
                a = models.WXUser.objects.filter(openid=_i.openid).first().id

            d1['info'] = "".join(str(usrinfo.usractive).split(" ")[1])
            d1['money'] = round(float(count) / 2000, 2) + Pcount
            d1['username'] = a
            d1['count'] = count
            d1['joincount'] = usercount
            l1.append(d1)
        return {"userdata": l1, 'total_count': total_count, FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {"userdata": None, 'total_count': None, FoundationConst.RN_RCODE: -1, FoundationConst.RN_RMSG: str(e)}


# 线下报名搜寻
@decorators.action_render
def SuchSign(request):
    try:
        now_page = int(request.POST['now_page'])
        page_rows = int(request.POST['page_rows'])
        start = (now_page - 1) * page_rows
        end = start + page_rows
        usrid = request.POST['id']
        if usrid is not None:
            offlinesign = models.UsrPhoneCall.objects.filter(id=usrid).all()
            totalcount = offlinesign.count()
            Getype = request.POST['type']
            if Getype == "1":
                l1 = []
                for i in offlinesign:
                    d1 = {}
                    d1['userid'] = i.id
                    _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.signuptime))
                    d1['updatetime'] = _time
                    d1['phonecall'] = i.usrsignup
                    l1.append(d1)
                excel = decorators.exportExcel(request, '线下报名', l1)
                return excel
            else:
                offlinesign = offlinesign[start: end]
                l1 = []

                for i in offlinesign:
                    d1 = {}
                    d1['userid'] = i.id
                    _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.signuptime))
                    d1['updatetime'] = _time
                    d1['phonecall'] = i.usrsignup
                    l1.append(d1)
                return {"signup": l1, 'total_count': totalcount, FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: None}
    except Exception as e:
        return {'signup': None, FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: str(e)}


@decorators.action_render
def ChangeCount(request):
    try:
        Cid = request.POST['Cid']
        CC = int(request.POST['change'].decode("gbk").encode("utf-8"))
        money = round(float(CC) / 2000, 2)
        Info = models.walkCount.objects.filter(id=Cid)
        _walk = models.weekCount.objects.filter(openid=Info[0].openid).filter(weekMatch=Info[0].weekMatch)
        walkData = _walk[0].walk + CC - Info[0].change
        _walk.update(walk=walkData)
        adminame = request.session.get('usrname')
        things = "管理员： " + str(adminame) + "修改用户步数为： " + str(CC) + "金钱变更为: " + str(money) + "原步数为: " + str(Info[0].walk) + " " + "active_id: " + str(Cid)
        activelog = models.AdminLog.objects.create(usrname=adminame, event=things)
        Info.update(money=str(money), change=CC)
        return {FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: "success"}
    except Exception as e:
        return {FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: str(e)}




# 改变pv uv
@decorators.action_render
def ChangePUv(request):
    try:
        addpv = request.POST['pv']
        adduv = request.POST['uv']
        PUv = models.CountPUV.objects.filter(id=1)
        adminame = request.session.get('usrname')
        THINGS = "管理员: " + adminame + "增加FAKE PV UV 为： " + addpv + " " + adduv + "原FAKE PV UV 数据为： " + PUv[0].addpv + " " + PUv[0].adduv
        PUv.update(addpv=addpv, adduv=adduv)
        models.AdminLog.objects.create(name=adminame, event=THINGS)
        return {FoundationConst.RN_RCODE: 0, FoundationConst.RN_RMSG: "success"}
    except Exception as e:
        return {FoundationConst.RN_RCODE: 1, FoundationConst.RN_RMSG: str(e)}

#
# @decorators.action_render
# def hitPrize(request):
#     try:
#         watchType = request.GET['type']
#         now = timezone.now()
#         dateTime = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, tzinfo=pytz.utc)
#         if watchType == "week":
#             hitprize = models.hitprize.objects.filter(creatime__gte=dateTime).filter(isSend=1).filter(countType=0).first()
#         elif watchType == "day":
#             hitprize = models.hitprize.objects.filter(creatime__gte=dateTime).filter(isSend=1).filter(
#                 countType=1).first()
#         else:
#             hitprize = models.hitprize.objects.filter(creatime__gte=dateTime).filter(isSend=1).filter(
#                 countType=3).first()
#         if hitprize is None:
#             return {"result_code": 1, "result_msg": None}
#         else:
#             prizeList = json.loads(hitprize.usrList)
#             return {"prizeList": prizeList, "result_code": 0, "result_msg": None, "id": hitprize.id}
#     except Exception as e:
#         return {"result_code": -1, "result_msg": e}


@decorators.action_render
def fetchmumber(request):
    try:
        allCount = models.hitprize.objects.all()
        l1 = []
        for i in allCount:
            d1 = {}
            d1['id'] = i.id
            d1['creatime'] = str(i.creatime)
            d1['countType'] = i.countType
            d1['isSend'] = i.isSend
            d1['weekMacht'] = i.weekMacht
            l1.append(d1)
        return {"countList": l1, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"countList": None, "result_code": -1, "result_msg": e}



#add
@decorators.action_render
def fetchDay(request):
    try:
        iD = request.GET['id']
        now_page = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        _Info = models.hitprize.objects.filter(id=iD)[0]
        weekMatch = _Info.weekMacht
        start = (now_page - 1) * page_rows
        end = start + page_rows
        Type = _Info.countType
        if Type == 0:
            UserData = models.weekCount.objects.filter(weekMatch=weekMatch).all().order_by('-walk')
            total_count = UserData.count()
            l1 = []
            count = 1
            if request.GET['type'] == '1':
                if total_count < 3000:
                    end = total_count
                else:
                    end = 3000
                for i in UserData[0: end]:
                    d1 = {}
                    d1['rank'] = count
                    count += 1
                    d1['usr'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['id'] = i.id
                    d1['walk'] = i.walk
                    d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=i.openid)[0].usractive.split(" ")[1])
                    d1['isSend'] = i.isSend
                    d1['countType'] = _Info.countType
                    d1['week'] = i.weekMatch
                    d1['creatime'] = str(_Info.creatime)
                    l1.append(d1)
                excel = decorators.exportExcel(request, "数据表", l1)
                return excel

            for i in UserData[start: end]:
                d1 = {}
                d1['rank'] = count
                d1['usr'] = models.WXUser.objects.filter(openid=i.openid).first().id
                d1['id'] = i.id
                d1['walk'] = i.walk
                d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=i.openid)[0].usractive.split(" ")[1])
                d1['isSend'] = i.isSend
                d1['countType'] = 0
                d1['week'] = weekMatch
                d1['creatime'] = str(_Info.creatime)
                count += 1
                l1.append(d1)
        else:
            now = datetime.date.today()
            Date = _Info.creatime.date()
            weekDay = Date - datetime.timedelta(days=1)
            valueList = models.walkCount.objects.filter(creaTime__gte=weekDay).filter(creaTime__lt=now).order_by('-change').all()
            total_count = valueList.count()
            l1 = []
            if now_page == 1:
                count = 1
            else:
                count = ((now_page - 1) * 5) + 1
            if request.GET['type'] == '1':
                if total_count < 3000:
                    end = total_count
                else:
                    end = 3000
                for i in valueList[0: end]:
                    d1 = {}
                    d1['rank'] = count
                    count += 1
                    d1['usr'] = models.WXUser.objects.filter(openid=i.openid).first().id
                    d1['id'] = i.id
                    d1['walk'] = i.change
                    d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=i.openid)[0].usractive.split(" ")[1])
                    d1['isSend'] = i.isGet
                    d1['countType'] = _Info.countType
                    d1['week'] = i.weekMatch
                    d1['creatime'] = str(_Info.creatime)
                    l1.append(d1)
                excel = decorators.exportExcel(request, "数据表", l1)
                return excel

            for i in valueList[start: end]:
                d1 = {}
                d1['rank'] = count
                count += 1
                d1['usr'] = models.WXUser.objects.filter(openid=i.openid).first().id
                d1['id'] = i.id
                d1['walk'] = i.change
                d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=i.openid)[0].usractive.split(" ")[1])
                d1['isSend'] = i.isGet
                d1['countType'] = _Info.countType
                d1['week'] = i.weekMatch
                d1['creatime'] = str(_Info.creatime)
                l1.append(d1)
        return {"priceList": l1, "result_code": 1, "result_msg": None, 'total_count': total_count}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}



@decorators.action_render
def fetchCount(request):
    try:
        now_page = int(request.POST['now_page'])
        page_rows = int(request.POST['page_rows'])
        id = request.POST['id']
        start = (now_page - 1) * page_rows
        end = start + page_rows
        valueList = models.hitprize.objects.filter(id=id).first()
        countList = json.loads(valueList.usrList)['data']
        if request.POST['type'] == "1":
            excel = decorators.exportExcel(request, "数据表", countList)
            return excel
        return {"priceList": countList[start: end], "total_count": len(countList), "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


# 发日奖
@decorators.action_render
def sendPrize(request):
    try:
        now = datetime.date.today()
        PRICESINFO = models.hitprize.objects.filter(creatime__gte=now).filter(countType=1).all()
        weekDay = now - datetime.timedelta(days=1)
        if not PRICESINFO:
            return {"result_code": 0, "result_msg": "error!!"}
        else:
            weekCount = PRICESINFO[0].weekMacht
            nowday = datetime.date.today()
            now = timezone.datetime.now()
            priceCount = models.qrcount.objects.filter(isend=1).filter(startime=str(datetime.date.today())).all()
            for i in priceCount:
                if i is None:
                    return {"result_code": -1, "result_msg": "没有奬卷"}
            if weekCount == 1:
                startTime = datetime.datetime.utcfromtimestamp(config.WorkConfig.starTime)
                startTime = datetime.datetime(startTime.year, startTime.month, startTime.day, 0, 0, 0, tzinfo=pytz.utc)
            elif weekCount == 2:
                startTime = datetime.datetime.utcfromtimestamp(config.WorkConfig.starTime)
                startTime = datetime.datetime(startTime.year, startTime.month, startTime.day, 0, 0, 0, tzinfo=pytz.utc)\
                            + datetime.timedelta(days=7)
            else:
                startTime = datetime.datetime.utcfromtimestamp(config.WorkConfig.starTime)
                startTime = datetime.datetime(startTime.year, startTime.month, startTime.day, 0, 0, 0,
                                              tzinfo=pytz.utc) + datetime.timedelta(days=14)
            priceList = []
            usrInfo = models.walkCount.objects.filter(creaTime__gte=weekDay, creaTime__lt=nowday, isGet=0).order_by(
                '-change').all()
            if usrInfo.count() >= 3000:
                end = 3000
            else:
                end = usrInfo.count()
            for i in usrInfo[:end]:
                d1 = {}
                d1['user'] = models.WXUser.objects.filter(openid=i.openid).first().id
                d1['id'] = i.id
                priceList.append(d1)
            for i, j in zip(priceList, priceCount):
                usrAlias = models.walkCount.objects.filter(id=i['id'])
                todayInfo = usrAlias.filter(creaTime__gte=datetime.date.today())
                if todayInfo.first() is not None:
                    todayInfo.update(isGet=1)
                usrAlias.update(priCode=j.id)
                models.qrcount.objects.filter(id=j.id).update(isend=0, sendTime=now)
            PRICESINFO.update(isSend=0)
            return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": 1, "result_msg": e}


# 生成总排名
@decorators.action_render
def allCount(request):
    try:
        nowDay = datetime.date.today()
        matchWeek = datetime.date.fromtimestamp(config.WorkConfig.starTime)
        priceInfo = models.hitprize.objects.filter(countType=2).all()
        l1 = []
        wxUser = models.WXUser.objects.all()
        for d in wxUser:
            d1 = {}
            d1['user'] = d.id
            d1['info'] = "".join(models.UsrPhoneCall.objects.filter(openid=d.openid)[0].usractive.split(" ")[1])
            count = 0
            walkInfo = models.walkCount.objects.filter(creaTime__gte=matchWeek).filter(creaTime__lte=nowDay).filter(openid=d.openid).all()
            for i in walkInfo:
                if int(i.change) != 0:
                    count += int(i.change)
                else:
                    count += int(i.walk)
            d1['walk'] = count
            l1.append(d1)
        count = 1
        if priceInfo[0] is None:
            for i in l1:
                models.hitprize.objects.create(
                    countType=2,
                    walk=i['walk'],
                    rank=count,
                    info=i['info'],
                    weekMacht=3,
                )
        else:
            models.hitprize.objects.filter(countType=2).all().delete()
            for i in l1:
                models.hitprize.objects.create(
                    countType=2,
                    walk=i['walk'],
                    rank=count,
                    info=i['info'],
                    weekMacht=3,
                )

        return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e  )}


# 生成周排名
@decorators.action_render
def makeWeek(request):
    try:
        nowDay = datetime.date.today()
        matchWek = int(str(nowDay - datetime.date.fromtimestamp(config.WorkConfig.starTime)).split(" ")[0])
        if 0 < matchWek <= 7:
            weekCount = 1

        elif 7 < matchWek <= 14:
            weekCount = 2
            matchWek -= 7
        else:
            weekCount = 3
            matchWek -= 14
        startday = nowDay - datetime.timedelta(days=matchWek)
        CountInfo = models.hitprize.objects.filter(countType=0).filter(weekMacht=weekCount).first()
        if CountInfo is not None:
            return {"result_code": 0, "result_msg": "已更新"}
        else:
            models.hitprize.objects.create(
                countType=0,
                isSend=1,
                weekMacht=weekCount
            )
            return {"result_code": 0, "result_msg": "已创建"}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


# 生成日排行
@decorators.action_render
def dayCount(request):
    try:
        nowDay = datetime.date.today()
        matchWek = int(str(nowDay - datetime.date.fromtimestamp(config.WorkConfig.starTime)).split(" ")[0])
        if 0 < matchWek <= 7:
            weekCount = 1

        elif 7 < matchWek <= 14:
            weekCount = 2
            matchWek -= 7
        else:
            weekCount = 3
            matchWek -= 14
        startday = nowDay - datetime.timedelta(days=matchWek)
        CountInfo = models.hitprize.objects.filter(countType=1).filter(creatime__gt=nowDay).filter(weekMacht=weekCount).first()
        if CountInfo is not None:
            return {"result_code": 0, "result_msg": "已更新"}
        else:
            models.hitprize.objects.create(
                countType=1,
                isSend=1,
                weekMacht=weekCount
            )
            return {"result_code": 0, "result_msg": "已创建"}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


# 确认周排名
@decorators.action_render
def accessWeek(request):
    try:
        _id = request.POST['id']
        models.hitprize.objects.filter(id=_id).all().update(isSend=0)
        return {"result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


@decorators.action_render
def fetchNowData(request):
    try:
        test = walkExcel.countDay(request)
        info = test.startDraw()
        return info
    except Exception as e:
        return {"result_code": e}



@decorators.action_render
def fakeData(request):
    try:
        password = request.GET['passwd']
        if password != "rua":
            return {"result_code": 2, "result_msg": "滚"}
        else:
            mumBer = int(request.GET['mum'])
            walkCount = request.GET['walkCount']

            nowDate = datetime.date.today() - datetime.timedelta(days=1)
            count = 0
            matchWek = int(str(nowDate - datetime.date.fromtimestamp(config.WorkConfig.starTime)).split(" ")[0])
            if 0 < matchWek <= 7:
                weekCount = 1
            elif 7 < matchWek <= 14:
                weekCount = 2
            else:
                weekCount = 3
            while count < mumBer:
                count += 1
                phoneNum = ""
                telList = [130, 131, 132, 155, 156, 186, 185, 134, 135, 137, 136, 138, 139, 150, 151, 152, 157, 158, 159
                    , 182, 183, 188, 187, 133, 153, 180, 181, 189]
                telHand = random.randint(0, len(telList) - 1)
                phoneNum += str(telList[telHand])
                for i in range(0, 8):
                    phoneNum += str(random.randint(0, 9))
                name = makeName.full_name(makeName.last_names, makeName.first_names)
                openid = "ssss$" + str(uuid.uuid4().hex)[0: 9]
                usrinfo = "手机号 " + phoneNum + " " + "姓名 " + name
                walk, Walk = walkCount.split(",")[0], walkCount.split(",")[1]
                walkNum = random.randint(int(walk), int(Walk))
                models.WXUser.objects.create(
                    openid=openid,
                    gender=0,
                    status=0
                )
                phoneCall = models.UsrPhoneCall.objects.create(
                    openid=openid,
                    usractive=usrinfo
                )
                info = models.walkCount.objects.create(
                    walk=walkNum,
                    change=walkNum,
                    money=round(float(walkNum) / 2000, 2),
                    image="http://www.fantizi5.com/zi/kt/e58187.jpg",
                    openid=openid,
                    info=phoneCall,
                    weekMatch=weekCount,
                    isGet=0
                )
                models.walkCount.objects.filter(id=info.id).update(creaTime=nowDate)
            return {"result_code": 0, "result_msg": "finish"}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}

@decorators.action_render
def delte(request):
    models.walkCount.objects.filter(priCode=615).update(priCode=None)
    models.walkCount.objects.filter(priCode=616).update(priCode=None)
    return {"result_msg": "success"}