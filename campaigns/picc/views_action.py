# -*- coding: utf-8 -*-
import math
from campaigns.picc.applet.REDIS import djangoCache
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.picc import models, config, const
from campaigns.foundation import wechat_api
from campaigns.picc.applet import decorators
from campaigns.picc.applet.vote import FendaVoteManager
from campaigns.picc.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos




@decorators.action_render
def random(request):
    try:
        l1 = []
        dreamInfo = models.Work.objects.all().order_by("votedCount")
        for i in dreamInfo:
            d1 = {}
            d1['id'] = i.id
            d1['name'] = i.name
            d1['lightime'] = str(i.lightime)
            d1['votecount'] = i.votedCount
            l1.append(d1)
        return {"dreamList": l1, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": str(e)}


@decorators.action_render
def vote(request):
    try:
        dreamId = request.POST['id']
        openid = request.session.get("wxUser")
        voteInfo = models.Vote.objects.filter(wxUser__openid=openid).first()
        if voteInfo is not None:
            return {"result_code": 1, "result_msg": "您已投过票"}
        else:
            wxUser = models.WXUser.objects.filter(openid=openid).first()
            dreamInfo = models.Work.objects.filter(id=dreamId).first()
            models.Vote.objects.create(
                    wxUser=wxUser,
                    work=dreamInfo,
                    status=10
                )
            nowCount = models.Work.objects.filter(id=dreamId)
            nowVote = nowCount[0].votedCount + 1
            nowCount.update(votedCount=dreamInfo.votedCount + 1)
            RedisCached = djangoCache(dreamId)
            nowCached = RedisCached.saveData(value=nowVote, save_type=3)
            return {"result_code": 0, "result_msg": nowCached}
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