# -*- coding: utf-8 -*-
import math, datetime, pytz, random
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.ycblank import models, config, const
from campaigns.ycblank import wechat_api
from campaigns.ycblank.applet import decorators
from campaigns.ycblank.applet.vote import FendaVoteManager
from campaigns.ycblank.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos
from django.utils import timezone
from collections import Counter
from campaigns.ycblank.applet.Tcos import Auth
from campaigns.ycblank.applet.getLocation import txLocations
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
def nickName(request):
    try:
        openid = request.GET['openid']
        if openid is not None:
            userinfo = models.WXUser.objects.filter(openid=openid)[0].nickname
            return {"result_code": 0, "result_msg": None, "nickname": userinfo}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


# 上传个人信息
@decorators.action_render
def uploadInfo(request):
    try:
        name = request.GET.get("name", None)
        phone = request.GET.get("phone", None)
        openid = request.session.get("wxUser")
        info = models.JsAuthor.objects.filter(phone=phone).first()
        if info.name is not None:
            return {"result_code": 1, "result_msg": "已有信息"}
        else:
            if name is not None and phone is not None:
                usrinfo = models.JsAuthor.objects.filter(openid=openid).update(name=name,
                    phone=phone)
                return {"result_code": 0, "result_msg": "done"}
            else:
                return {"result_code": 2, "result_msg": "without_user_message"}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


# 初始生成红包检测是否有未完成红包
@decorators.action_render
def chance(request):
    try:
        openid = request.session.get("wxUser")
        print openid
        finishInfo = models.prizePool.objects.filter(hasFinished=False, master__openid=openid).first()
        today = datetime.date.today()
        torrmor = today + datetime.timedelta(days=1)
        if finishInfo is not None:
            return {"result_code": 1, "result_msg": "用户具有未完成作品", "id": finishInfo.id, "unitBit": finishInfo.unitBit, "decade": finishInfo.decade,
                    'hundreds': finishInfo.hundreds, 'decadeOpenid': finishInfo.decadeOpenid, 'hundredOpenid': finishInfo.hundredOpenid}

        elif models.prizePool.objects.filter(creatime__gte=today, creatime__lt=torrmor, hasFinished=True, master__openid=openid).first() is not None:
            finishInfo = models.prizePool.objects.filter(creatime__gte=today, creatime__lt=torrmor, hasFinished=True, master__openid=openid).first()
            return {"result_code": 3, "result_msg": "今天已参与过", "id": finishInfo.id, "unitBit": finishInfo.unitBit, "decade": finishInfo.decade,
                    'hundreds': finishInfo.hundreds, 'decadeOpenid': finishInfo.decadeOpenid, 'hundredOpenid': finishInfo.hundredOpenid}

        else:
            rankinfo = models.prizePool.objects.filter(master__openid=openid).order_by('-rank').first()
            if rankinfo is not None:
                rank = rankinfo.rank + 1
            else:
                rank = 1
            usr = models.JsAuthor.objects.filter(openid=openid).first()
            if usr is None:
                usr = models.JsAuthor.objects.create(
                    openid=openid
                )
            startChance = cache.get("ychance")
            endChance = cache.get("echance")
            chance = random.randint(int(startChance), int(endChance))
            iphoneInfo = models.peasCount.objects.filter(peasType=2).first()
            if chance == 6666 and iphoneInfo.peaSend < iphoneInfo.Count and models.prizePool.objects.filter(master__openid=openid, luckChance="00").first() is None\
                     and models.prizePool.objects.filter(creatime__gte=datetime.date.today(), luckChance="00").all().count() < models.peasCount.objects.filter(peasType=2).first().max_send:
                luckChance="00"
                nowsend = iphoneInfo.peaSend + 1
                models.peasCount.objects.filter(peasType=2).update(peaSend=nowsend)

            elif models.peasCount.objects.filter(peasType=0).first().peaSend >= 799510:
                return {"result_code": 4, "result_msg": "活动奖品为空 活动结束"}

            else:
                decade = random.randint(5, 9)
                hundred = random.randint(0, 4)
                luckChance = str(decade) + str(hundred)
                nowsend = models.peasCount.objects.filter(peasType=0).first().peaSend + int(luckChance[1] + luckChance[0] + "0")
                models.peasCount.objects.filter(peasType=0).update(peaSend=nowsend)

            finishInfo = models.prizePool.objects.create(
            master=usr,
            rank=rank,
            luckChance=luckChance
            )
            return {"result_code": 0, "result_msg": "创建新作品", "id": finishInfo.id, "unitBit": finishInfo.unitBit, "decade": finishInfo.decade,
                    'hundreds': finishInfo.hundreds, 'decadeOpenid': finishInfo.decadeOpenid, 'hundredOpenid': finishInfo.hundredOpenid}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}



# 个人打开个位红包
@decorators.action_render
def unit(request):
    try:
        id = request.GET['id']
        openid = request.session.get("wxUser")
        such = request.GET.get("such", None)
        dataInfo = models.prizePool.objects.filter(id=id).first()
        if such is None:
            if dataInfo.master.openid == openid:
                isSelf = 0
            else:
                isSelf = 1
            return {"result_code": 20, "result_msg": "show_data", "isSelf": isSelf, "id": dataInfo.id, "unitBit": dataInfo.unitBit,
                    "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished, 'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}

        if dataInfo.master.openid != openid:
            return {"result_code": 2, "result_msg": "not_self", "id": dataInfo.id, "unitBit": dataInfo.unitBit, "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished, 'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
        elif dataInfo.unitBit is not None:
            return {"result_code": 1, "result_msg": "already cache", "id": dataInfo.id, "unitBit": dataInfo.unitBit, "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished, 'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
        else:
            wxa = models.prizePool.objects.filter(id=id)
            wxa.update(unitBit="0")
            return {"result_code": 0, "result_msg": None, "id": wxa[0].id, "unitBit": wxa[0].unitBit, "decade": wxa[0].decade,
                    'hundreds': wxa[0].hundreds, 'hasFinish': wxa[0].hasFinished, 'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


# 分享他人打开红包
@decorators.action_render
def shareOther(request):
    try:
        id = request.GET['id']
        openid = request.session.get("wxUser")
        such = request.GET.get("such", None)
        dataInfo = models.prizePool.objects.filter(id=id).first()
        if such is None:
            if dataInfo.master.openid == openid:
                isSelf = 0
            else:
                isSelf = 1
            if dataInfo.decadeOpenid == openid:
                clickDecade = 0
            else:
                clickDecade = 1
            if dataInfo.hundredOpenid == openid:
                clickhundred = 0
            else:
                clickhundred = 1
            return {"result_code": 20, "result_msg": "show_data", "isSelf": isSelf, "id": dataInfo.id, "unitBit": dataInfo.unitBit,
                    "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished, 'Clickdecade': clickDecade, 'Clickhundred': clickhundred,
                    'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
        if dataInfo.master.openid == openid:
            return {"result_code": 2, "result_msg": "is_self", "id": dataInfo.id, "unitBit": dataInfo.unitBit, "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished,
                    'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
        elif dataInfo.unitBit is None:
            return {"result_code": 3, "result_msg": "not_unit", "id": dataInfo.id, "unitBit": dataInfo.unitBit, "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished,
                    'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}

        elif dataInfo.decade is None:
            wxa = models.prizePool.objects.filter(id=id)
            wxa.update(
                decade=models.prizePool.objects.filter(id=id).first().luckChance[0], decadeOpenid=request.session.get('wxUser'))
            return {"result_code": 0, "result_msg": "success", "id": wxa[0].id, "unitBit": wxa[0].unitBit,
                    "decade": wxa[0].decade,
                    'hundreds': wxa[0].hundreds, 'hasFinish': wxa[0].hasFinished,
                    'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}

        elif dataInfo.hundreds is None:
            if request.session.get("wxUser") == dataInfo.decadeOpenid:
                return {"result_code": 100, "result_msg": "same_user", "id": dataInfo.id, "unitBit": dataInfo.unitBit,
                    "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished,
                        'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
            wxa = models.prizePool.objects.filter(id=id)
            wxa.update(
                hundreds=models.prizePool.objects.filter(id=id).first().luckChance[1], hundredOpenid=openid)
            return {"result_code": 0, "result_msg": "success", "id": wxa[0].id, "unitBit": wxa[0].unitBit,
                    "decade": wxa[0].decade,
                    'hundreds': wxa[0].hundreds, 'hasFinish': wxa[0].hasFinished,
                    'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
        else:
            return {"result_code": 4, "result_msg": "not_unit", "id": dataInfo.id, "unitBit": dataInfo.unitBit,
                    "decade": dataInfo.decade,
                    'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished,
                    'decadeOpenid': dataInfo.decadeOpenid, 'hundredOpenid': dataInfo.hundredOpenid}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


# 更改完成状态
@decorators.action_render
def getFinish(request):
    try:
        id = request.GET['id']
        openid = request.session.get('wxUser')
        user = models.JsAuthor.objects.filter(openid=openid).first()
        dataInfo = models.prizePool.objects.filter(id=id).first()
        if dataInfo.master.openid != openid:
            return {'result_code': 1, "result_msg": 'not_self'}
        elif dataInfo.hasFinished is True:
            return {"result_code": 2, "result_msg": "is Done"}
        elif user.name is None:
            return {"result_code": 7, "result_msg": "bad post"}
        else:
            info = models.prizePool.objects.filter(id=id).first()
            if info.luckChance == "00":
                models.jsPrizes.objects.create(
                    user=user,
                    peasType=2,
                    Count=1
                )
                models.prizePool.objects.filter(id=id).update(hasFinished=True)
            else:
                models.jsPrizes.objects.create(
                    user=user,
                    peasType=0,
                    Count=int(info.luckChance[1] + info.luckChance[0] + "0")
                )
                models.JsAuthor.objects.filter(openid=openid).update(
                    jsSyd=user.jsSyd + int(info.luckChance[1] + info.luckChance[0] + "0")
                )
                models.prizePool.objects.filter(id=id).update(hasFinished=True)
            return {"result_code": 0, "result_msg": "SUCCESS", "id": dataInfo.id, "unitBit": dataInfo.unitBit,
                "decade": dataInfo.decade,
                'hundreds': dataInfo.hundreds, 'hasFinish': dataInfo.hasFinished}

    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}

@decorators.action_render
def checkSelf(request):
    try:
        openid = request.session.get("wxUser")
        allData = models.jsPrizes.objects.filter(user__openid=openid).all()
        l1 = []
        hasIphone = False
        allCount = 0
        for i in allData:
            d1 = {}
            if i.peasType == 2:
                hasIphone = True
            if i.peasType == 0:
                allCount += i.Count
            d1['peasType'] = i.peasType
            d1['Count'] = i.Count
            d1['creatime'] = str(i.creatime)
            l1.append(d1)
        return {'result_code': 0, 'result_msg': None, "dataList": l1, "allPeas": allCount, "hasIphone": hasIphone}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}

@decorators.action_render
def getChace(request):
    try:
        start = request.GET['start']
        passwd = request.GET['passwd']
        if passwd != "13770701228":
            return {"result": "get out"}
        else:
            end = request.GET['end']
            cache.set("ychance", int(start), 60*60*60*60)
            cache.set("echance", int(end), 60*60*60*60)
            return {"result": "done"}
    except Exception as e:
        return {"exception": str(e)}