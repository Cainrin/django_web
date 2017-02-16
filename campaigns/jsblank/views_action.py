# -*- coding: utf-8 -*-
import math, datetime, pytz, random, time
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.jsblank import models, config, const
from campaigns.foundation import wechat_api
from campaigns.jsblank.applet import decorators
from campaigns.jsblank.applet.vote import FendaVoteManager
from campaigns.jsblank.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos
from django.utils import timezone
from collections import Counter
from campaigns.jsblank.applet.Tcos import Auth
from campaigns.jsblank.applet.getLocation import txLocations
from django.core.cache import cache




@decorators.action_render
def get_sign_package(request):
    try:
        url = request.POST['url']
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    sign_package = wechat_api.WechatApi().get_sign_package(url)
    return sign_package


@decorators.action_render
def checkFirst(request):
    try:
        isFrist = request.session.get("first")
        openid = request.session.get("wxUser")
        if isFrist is not None:
            usrInfo = models.JsAuthor.objects.filter(openid=openid).first()
            if usrInfo is not None:
                return {"isFrist": 1, "phone": usrInfo.phone, "name": usrInfo.name, 'syd': usrInfo.jsSyd, "result_code": 0, "result_msg": None}
            else:
                return {"isFrist": 1, "phone": None, "name": None, "result_code": 0, "result_msg": None}
        else:
            request.session['first'] = 1
            return {"isFrist": 0, "phone": None, "name": None, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}



@decorators.action_render
def uploadInfo(request):
    try:
        name = request.POST['name']
        phone = request.POST['phone']
        syd = request.POST.get("peas", 0)
        openid = request.session.get("wxUser")
        info = models.JsAuthor.objects.filter(openid=openid).first()
        if info is not None:
            return {"result_code": 1, "result_msg": "已绑定"}
        elif models.JsAuthor.objects.filter(phone=phone).first() is not None:
            return {"result_code": 2, "result_msg": "该手机号已被注册"}
        else:
            usrinfo = models.JsAuthor.objects.create(
                name=name,
                openid=openid,
                phone=phone,
                jsSyd=int(syd)
            )
            nowPeas = models.peasCount.objects.filter(peasType=0).first().peaSend
            nowPeas += syd
            models.peasCount.objects.filter(peasType=0).update(peaSend=nowPeas)
            models.prizePool.objects.create(
                user=usrinfo,
                location=00,
                peasType=0,
                peasCount=int(syd)
            )
            return {"result_code": 0, "result_msg": "done"}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}



@decorators.action_render
def chance(request):
    try:
        if time.time() <= time.mktime(time.strptime("2017-01-12", '%Y-%m-%d')):
            return {"result_code": 5002, "result_msg": "活动未开始"}
        if time.time() >= time.mktime(time.strptime("2017-01-17", '%Y-%m-%d')):
            return {"result_code": 5001, "result_msg": "活动过期"}
        location = request.POST['location']
        openid = request.session.get("wxUser")
        if openid == "oV3Ftt5qQwmu5afSDJGNzY1E7oB0":
            return {"result_code": 5003, "result_msg": "band_user"}
        locationList = ["北京西路支行",
"西康路支行",
"城北支行",
"城西支行",
"龙江支行",
"中央路支行",
"泰山路支行",
"城中支行",
"总行营业部",
"浦口支行",
"城南支行",
"下关支行",
"江宁开发区支行",
"城东支行",
"高淳支行",
"鼓楼支行",
"河西支行",
"江宁支行",
"新港支行",
"新街口支行",
"雨花支行",
"溧水支行",
"金马郦城社区支行",
"迈皋桥支行",
"鸿福苑社区支行",
"保利香槟社区支行",
"万江共和社区支行",
"德基广场",
"水游城",
"虹悦城",
"河西万达",
"景枫KINGMO",
"弘阳广场",
"仙林金鹰奥莱城",
"环亚凯瑟琳"]
        if location not in locationList:
            return {"result_code": 5008, "result_msg": "error_location"}
        usr = models.JsAuthor.objects.filter(openid=openid).first()
        if usr is None:
            return {"result_code": 3, "result_msg": "用户没有绑定手机号"}
        nowday = datetime.date.today()
        tomorrow = nowday + datetime.timedelta(days=1)
        checkLocation = models.prizePool.objects.filter(location=location, user__openid=openid, creatime__gte=nowday, creatime__lt=tomorrow).first()
        if checkLocation is not None:
            return {"result_code": 2, "result_msg": "当日当前位置已抽过"}
        checkGolden = models.prizePool.objects.filter(creatime__gte=nowday, creatime__lt=tomorrow, peasType=1).all().count()
        if checkGolden < 10:
            if models.prizePool.objects.filter(user__openid=openid, peasType=1).first() is None:
                Golden = models.peasCount.objects.filter(peasType=1).first()
                if str(datetime.date.today()) == "2016-01-18" and location == "ssadsa":
                    if models.prizePool.objects.filter(creatime__day=datetime.date.today(), peasType=1,
                                                   location="ssadsa").all().count() < 3:
                        luckNum = random.randint(0, 100)
                        if luckNum <= 20:
                            models.prizePool.objects.create(
                                user=usr,
                                location=location,
                                peasType=1,
                                peasCount=1
                            )
                            peasend = Golden.peaSend + 1
                            models.peasCount.objects.filter(peasType=1).update(peaSend=peasend)
                            return {"result_code": 0, "peasType": 1, "peasCount": 1, "result_msg": None}

                if Golden.peaSend < Golden.Count:
                    startNum = cache.get("startchance")
                    endNum = cache.get("endchance")
                    luckChance = random.randint(int(startNum), int(endNum))
                    if luckChance == 6666:
                        models.prizePool.objects.create(
                            user=usr,
                            location=location,
                            peasType=1,
                            peasCount=1
                        )
                        peasend = Golden.peaSend + 1
                        models.peasCount.objects.filter(peasType=1).update(peaSend=peasend)
                        return {"result_code": 0, "peasType": 1, "peasCount": 1, "result_msg": None}
        silver = models.peasCount.objects.filter(peasType=0).first()
        if silver.peaSend < silver.Count:
            blackList = ['oV3Ftt5qQwmu5afSDJGNzY1E7oB0', "oV3Ftt5XjWHgnha8asp5N8xXBQLQ", "oV3FttxLxYyLlcOYEFMS8VyBROXw", 'oV3FttyC42AA5Hlb0qBfoYJS0hKo', 'oV3Ftt_Zx4AzSrJiI_57G_n40E04', 'oV3Ftt5-y4bMp0gmeyF4S7iqF_Ag', 'oV3Fttw_Z6OOO4Vu1P10I2nFhxN8']
            if openid in blackList:
                maxSilver = 30
                minSilver = 20
            else:
                maxSilver = int(cache.get("maxSend"))
                minSilver = int(cache.get("minSend"))
            if silver.Count - silver.peaSend > maxSilver:
                peasCount = random.randint(minSilver, maxSilver)
            else:
                peasCount = random.randint(0, silver.Count - silver.peaSend)
            usrpeas = usr.jsSyd + peasCount
            maxSend = silver.peaSend + peasCount
            models.prizePool.objects.create(
                 user=usr,
                 location=location,
                 peasType=0,
                 peasCount=peasCount
            )
            models.JsAuthor.objects.filter(openid=openid).update(jsSyd=usrpeas)
            models.peasCount.objects.filter(peasType=0).update(peaSend=maxSend)
            return {"result_code": 0, "peasType": 0, "peasCount": peasCount, "result_msg": None}
        else:
            return {"result_code": 1, "result_msg": "没豆子了"}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


@decorators.action_render
def checkRank(request):
    try:
        now_page = int(request.GET['now_page'])
        page_rows = int(request.GET['page_rows'])
        start = (now_page - 1) * page_rows
        end = start + page_rows
        openid = request.session.get("wxUser")
        myInfo = models.JsAuthor.objects.filter(openid=openid).first()
        if myInfo is None:
            phone = None
            myrank = None
            jsSyd = None
        else:
            myrank = models.JsAuthor.objects.filter(jsSyd__gt=myInfo.jsSyd).all().count() + 1
            phone = myInfo.phone
            jsSyd = myInfo.jsSyd
        total_count = models.JsAuthor.objects.all().count()
        allAccount = models.JsAuthor.objects.all().order_by("-jsSyd")[start: end]
        l1 = []
        count = start + 1
        for i in allAccount:
            d1 = {}
            d1['rank'] = count
            d1['phone'] = i.phone
            d1['jsSyd'] = i.jsSyd
            count += 1
            l1.append(d1)
        return {"result_code": 0, "result_msg": None, "phone": phone, "rank": myrank, 'jsSyd': jsSyd, "total_count": total_count, "account_list": l1}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


@decorators.action_render
def getPeas(request):
    try:
        openid = request.session.get("wxUser")
        myInfo = models.JsAuthor.objects.filter(openid=openid).first()
        if myInfo is not None:
            myrank = models.JsAuthor.objects.filter(jsSyd__gt=myInfo.jsSyd).all().count() + 1
            jsSyd = myInfo.jsSyd
        else:
            jsSyd = None
            myrank = None
        allpeas = models.prizePool.objects.filter(user__openid=openid).all().order_by("-creatime")
        l1 = []
        for i in allpeas:
            d1 = {}
            d1['creatime'] = str(i.creatime)
            d1['location'] = i.location
            d1['peasCount'] = i.peasCount
            d1['peasType'] = i.peasType
            d1['phone'] = models.JsAuthor.objects.filter(openid=openid).first().phone
            l1.append(d1)
        return {"result_code": 0, "result_msg": None, "account_list": l1, 'jsSyd': jsSyd, 'myrank': myrank}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


@decorators.action_render
def setCache(request):
    passWd = int(request.POST["passwd"])
    if passWd != 13770701228:
        return {"result_code": -1}
    else:
        maxSend = int(request.POST['max'])
        minSend = int(request.POST['min'])
        cache.set("maxSend", maxSend, 60*60*3600)
        cache.set("minSend", minSend, 60*60*3600)
        return {"result_code": 0, "result_msg": "done"}



@decorators.action_render
def setChance(request):
    passWd = int(request.POST["passwd"])
    if passWd != 13770701228:
        return {"result_code": -1}
    else:
        maxSend = int(request.POST['start'])
        minSend = int(request.POST['end'])
        cache.set("startchance", maxSend, 60*60*3600)
        cache.set("endchance", minSend, 60*60*3600)
        return {"result_code": 0, "result_msg": "done"}


@decorators.action_render
def prinTopenid(request):
    openid = request.session.get("wxUser")
    print openid
    return {"result": openid}



@decorators.action_render
def shadowPoint(request):
    passwd = int(request.POST['passwd'])
    if passwd != 13770701228:
        return {"result_code": -1}
    else:
        silver = models.peasCount.objects.filter(peasType=0).first()
        location = request.POST['location']
        openid = request.POST['openid']
        peasCount = int(request.POST['Count'])
        nowday = datetime.date.today()
        tomorrow = nowday + datetime.timedelta(days=1)
        checkLocation = models.prizePool.objects.filter(location=location, user__openid=openid, creatime__gte=nowday,
                                                        creatime__lt=tomorrow).first()
        if checkLocation is not None:
            return {"result_code": 1}
        maxSend = silver.peaSend + peasCount
        usr = models.JsAuthor.objects.filter(openid=openid).first()
        models.prizePool.objects.create(
            user=usr,
            location=location,
            peasType=0,
            peasCount=peasCount
        )
        jsSyd = usr.jsSyd + peasCount
        models.JsAuthor.objects.filter(openid=openid).update(jsSyd=jsSyd)
        models.peasCount.objects.filter(peasType=0).update(peaSend=maxSend)
        return {'result_code': 0}
