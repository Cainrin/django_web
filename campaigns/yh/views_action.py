# -*- coding: utf-8 -*-
import math, datetime, pytz, random
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.yh import models, config, const
from campaigns.foundation import wechat_api
from campaigns.yh.applet import decorators
from campaigns.yh.applet.vote import FendaVoteManager
from campaigns.yh.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos
from django.utils import timezone
import uuid, time
from collections import Counter
from campaigns.yh.applet.Tcos import Auth
import json


@decorators.action_render
def Fakeupload(request):
    try:
        usrDream = request.POST['String'].encode("utf-8")
        usrImage = request.POST['Image'].encode("utf-8")
        usrName = request.POST['name'].encode("utf-8")
        openid = "WHYC$" + str(uuid.uuid4().hex)[0: 11]
        usrId = models.WXUser.objects.create(openid=openid,
                                             gender=0,
                                             status=10)
        authorUsr = models.Author.objects.create(wxUser=usrId)
        usrWork = models.Work.objects.create(
            type=0,
            name=usrName,
            string=usrDream,
            imageurl=usrImage,
            author=authorUsr,
            status=10,
        )
        return {"result_code": 0, "result_msg": "SUCCESS", "id": usrWork.id}
    except Exception as e:
        return {"result_code": 1, "result_msg": str(e)}


# 上传
@decorators.action_render
def upload(request):
    try:
        # endTime = "2016-11-18 15:30:00"
        # timeEnd = time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S'))
        # if int(time.time()) >= timeEnd:
        #     return {"result_code": 0, "result_msg": "活动已结束"}
        usrDream = request.POST['String'].encode("utf-8")
        usrImage = request.POST['Image'].encode("utf-8")
        usrName = request.POST['name'].encode("utf-8")
        usrId = request.session.get("wxUser")
        usninfo = models.Work.objects.filter(author__wxUser__openid=usrId).first()
        if usninfo is None:
            usrId = models.WXUser.objects.filter(openid=usrId).first()
            authorUsr = models.Author.objects.create(wxUser=usrId)
            usrWork = models.Work.objects.create(
                type=0,
                name=usrName,
                string=usrDream,
                imageurl=usrImage,
                author=authorUsr,
                status=10,
            )
            return {"result_code": 0, "result_msg": "SUCCESS", "id": usrWork.id}
        else:
            print usninfo
            return {"result_code": 1, "result_msg": "您已上传过"}
    except Exception as e:
        return {"result_code": 1, "result_msg": str(e)}



# 随机梦想
@decorators.action_render
def random_dream(request):
    try:
        l1 = []
        dreamId = models.Work.objects.all()
        for i in dreamId:
            l1.append(i.id)
        randomDream = l1[random.randint(0, len(l1) - 1)]
        workDream = models.Work.objects.get(id=randomDream)
        return {"name": workDream.name, "id": workDream.id, "String": workDream.string, "Image": str(workDream.imageurl), "vote": workDream.votedCount, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}




@decorators.action_render
def fetch_dream(request):
    try:
        now_page = int(request.POST['nowPage'])
        page_rows = int(request.POST['pageRows'])
        total_count = models.Work.objects.filter(status=FoundationConst.STATUS_ONLINE).count()
        total_pages = int(math.ceil(float(total_count) / float(page_rows)))
        start = (now_page - 1) * page_rows
        end = start + page_rows
        workList = models.Work.objects.filter(status=FoundationConst.STATUS_ONLINE).all().order_by('-votedCount')[start: end]
        l1 = []
        for i in workList:
            d1 = {}
            d1['name'] = i.name
            d1['id'] = i.id
            d1['String'] = i.string
            d1['Image'] = str(i.imageurl)
            d1['vote'] = i.votedCount
            l1.append(d1)
        return {"worklist": l1, "total_pages": total_pages, "result_code": 0, "result_msg": None}
    except Exception as e:
        return {"result_code": 1, "result_msg": e}




@decorators.action_render
def dreamVote(request):
    try:
        endTime = "2016-11-18 15:30:00"
        timeEnd = time.mktime(time.strptime(endTime, '%Y-%m-%d %H:%M:%S'))
        if int(time.time()) >= timeEnd:
            return {"result_code": 0, "result_msg": "活动已结束"}
        voteId = request.POST['id']
        usrInfo = request.session.get("wxUser")
        now = datetime.date.today()
        voteDream = models.Vote.objects.filter(creationTime__gte=now).filter(wxUser__openid=usrInfo).all().count()
        if voteDream >= 3:
            return {"result_code": 1, "result_msg": "您今天已经投过票"}
        else:
            dreamWork = models.Work.objects.filter(id=voteId).first()
            wxUser = models.WXUser.objects.filter(openid=usrInfo).first()
            models.Vote.objects.create(
                work=dreamWork,
                wxUser=wxUser,
                status=10
            )
            nowVote = dreamWork.votedCount + 1
            dreamWork = models.Work.objects.filter(id=voteId).update(votedCount=nowVote)
            return {"result_code": 0, "result_msg": "SUCCESS"}
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
def such_work(request):
    try:
        work_id = request.GET['id']
        workDream = models.Work.objects.filter(id=work_id).first()
        OPENID = request.session.get("wxUser")
        if workDream is not None:
            if OPENID == workDream.author.wxUser.openid:
                isSelf = 0
            else:
                isSelf = 1
            return {"name": workDream.name, "id": workDream.id, "String": workDream.string,
                    "Image": str(workDream.imageurl), "vote": workDream.votedCount, "isSelf": isSelf, "result_code": 0, "result_msg": None}
        else:
            return {"result_code": 1, "result_msg": None}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


@decorators.action_render
def fetch_self(request):
    try:
        wxUser = request.session.get("wxUser")
        usrDream = models.Work.objects.filter(author__wxUser__openid=wxUser).first()
        if usrDream is not None:
            return {"String": usrDream.string, "name": usrDream.name, "image": str(usrDream.imageurl), "id": usrDream.id, "vote": usrDream.votedCount
                ,"result_code": 0, "result_msg": None, "phone": usrDream.author.cellphone}
        else:
            return {"result_code": 1, "result_msg": "未上传"}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


@decorators.action_render
def finish(request):
    try:
        phone = request.POST['phone']
        wxUser = request.session.get("wxUser")
        usrDream = models.Author.objects.filter(wxUser__openid=wxUser).update(cellphone=phone)
        return {"result_code": 0, "result_msg": "success"}
    except Exception as e:
        return {"result_code": -1, "result_msg": e}


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


#add
@decorators.action_render
def addWork(request):
    try:
        passwd = request.GET['passwd']
        if passwd != 'RUARUARUA':
            return {"result_msg": "滚"}
        else:
            imageURL = request.GET['url']
            rank = request.GET['rank']
            models.ranDomWork.objects.create(
                imageurl=imageURL,
                rank=rank
            )
            return {"result_code": 0}
    except Exception as e:
        return {"result_code": 1, "result_msg": str(e)}



@decorators.action_render
def fatchDream(request):
    try:
        count = int(request.GET['count'])
        wxUser = request.session.get("wxUser")
        if count < 50:
            workinfo = models.ranDomWork.objects.filter(rank=count).first()
            return {"imageUrl": str(workinfo.imageurl), "rank": workinfo.rank, "id": workinfo.id, "openid": wxUser, "result_code": 0, "result_msg": None}
        else:
            return {"result_code": 1, "result_msg": "no more pictures"}
    except Exception as e:
        return {"result_code": 1, "result_msg": str(e)}




@decorators.action_render
def suchDream(request):
    ID = request.GET['id']
    openid = request.GET['openid']
    if openid == request.session.get("wxUser"):
        return {"result_code": 1, "result_msg": None}
    else:
        workinfo = models.ranDomWork.objects.filter(id=ID).first()
        return {"result_code": 0, "result_msg": None, "imageUrl": str(workinfo.imageurl), "rank": workinfo.rank, "id": workinfo.id, "openid": request.session.get("wxUser")}


@decorators.action_render
def isExcel(request):
    locaData = models.Work.objects.all().order_by('id')
    page_Count = request.GET.get("pageCount", None)
    page, count = page_Count.split(",")[0], page_Count.split(",")[1]
    l1 = []
    for i in locaData[int(page): int(count)]:
        d1 = {}
        d1['名字'] = i.name
        d1['梦想'] = i.string
        d1['图片url'] = str(i.imageurl)
        if i.author.cellphone is not None:
            d1['手机号'] = i.author.cellphone
        else:
            d1['手机号'] = None
        d1['状态'] = i.status
        d1['票数'] = i.votedCount
        d1['创建时间'] = i.creationTime
        l1.append(d1)
    excel = decorators.exportExcel(request, "洋河数据表", l1)
    return excel



@decorators.action_render
def ranDoMdream(request):
    try:
        wxUser = request.session.get('wxUser')                                                      # 获得openid
        if request.session.get("first") is None or request.session.get("first") is True:           # 判断用户是否为是起始循环
            randomList = []                                                                         # 如果是创建空列表
            dreamList = models.ranDomWork.objects.all().values_list('id', flat=True)                # 生成现有所有梦想id列表集合
            randomValue = random.randint(0, len(dreamList) - 1)                                     # 随机抽取下标值
            randomList.append(dreamList[randomValue])                                               # 抽取到的id放入空列表
            request.session['randomList'] = json.dumps(randomList)                                  # 将列表存入session
            request.session['first'] = False                                                        # 初始循环值为False
            workinfo = models.ranDomWork.objects.filter(id=str(dreamList[randomValue])).first()     # 查数据返回
            return {"imageUrl": str(workinfo.imageurl), "rank": workinfo.rank, "id": workinfo.id, "openid": wxUser,
                    "result_code": 0, "result_msg": None}
        else:
            randomList = json.loads(request.session.get("randomList"))                              # 获取用户已浏览过的列表
            dreamList = models.ranDomWork.objects.all().values_list('id', flat=True)                # 生成现有所有梦想id列表集合
            sumList = list(set(dreamList) - set(randomList))                                        # 取差集
            if sumList:                                                                             # 如果差集列表不为空
                randomValue = random.randint(0, len(sumList) - 1)                                   # 随机抽取列表下标值
                randomList.append(sumList[randomValue])                                             # 增加浏览列表id值
                request.session['randomList'] = json.dumps(randomList)                              # 存入session
                request.session['first'] = False                                                    # 起始循环为False
                workinfo = models.ranDomWork.objects.filter(id=sumList[randomValue]).first()        # 查数据返回
                return {"imageUrl": str(workinfo.imageurl), "rank": workinfo.rank, "id": workinfo.id, "openid": wxUser,
                        "result_code": 0, "result_msg": None}
            else:
                request.session['randomList'] = json.dumps(randomList)                              # 如果差集为空
                request.session['first'] = True                                                     # 起始循环为真下轮进入新loops
                return {"result_code": 1, "result_msg": "已无更多奖品"}
    except Exception as e:
        print e
        return {"result_code": -1, "result_msg": str(e)}



