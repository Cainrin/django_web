# -*- coding: utf-8 -*-
import math, hashlib, json, base64
from campaigns.foundation import wechat_api
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.yiquan import models, config, const
from campaigns.yiquan.applet import decorators
from campaigns.yiquan.applet import regenerate
from campaigns.yiquan.applet import utils as yiquan_utils
from campaigns.yiquan.Views_Page import mobile_page_myproduct
from django.http import HttpResponse
from campaigns.yiquan.applet.vote import YiQuanVoteManager


# 展示作品
@decorators.action_render
def pc_fetch_works(request):
    try:
        now_page = int(request.POST['nowPage'])
        page_rows = int(request.POST['pageRows'])
        order_by_votes = request.POST.get('orderByVotes', False)
        order_by_date = request.POST.get('orderByDate', False)
        search_key_words = request.POST.get('searchKeyWords', None)
    except Exception as e:
        raise utils.ClientException(str(e))
    total_pages = 0
    work_list = None
    if search_key_words is not None:
        pk_work = None
        try:
            maybe_id = int(search_key_words)
            pk_work = models.YQWork.objects.get(pk=maybe_id)
        except:
            pass
        total_count = models.YQWork.objects.filter(status=FoundationConst.FIX).filter(id__contains=search_key_words).count()
        total_pages = int(math.ceil(float(total_count) / float(page_rows)))
        start = (now_page - 1) * page_rows
        end = start + page_rows
        work_list = models.YQWork.objects.filter(fixstatus=FoundationConst.FIX).filter(id__contains=search_key_words).all()[start: end]
        if pk_work is not None:
            new_work_list = [pk_work]
            for work in work_list:
                if pk_work.id != work.id:
                    new_work_list.append(work)
            work_list = new_work_list
        if len(work_list) != 0 and total_pages == 0:
            total_pages = 1
    else:
        if order_by_date:
            order_key = '-creationTime'
        else:
            order_key = '-votedCount'
        total_count = models.YQWork.objects.filter(fixstatus=FoundationConst.FIX).order_by(order_key).count()
        total_pages = int(math.ceil(float(total_count) / float(page_rows)))
        start = (now_page - 1) * page_rows
        end = start + page_rows
        work_list = models.YQWork.objects.filter(fixstatus=FoundationConst.FIX).order_by(order_key).all()[start: end]
    work_list = yiquan_utils.fit_up_work_list(work_list)
    return {
        FoundationConst.RN_TOTAL_PAGES: total_pages,
        FoundationConst.RN_WORK_LIST: work_list
    }


# workid搜寻
@decorators.action_render
def pc_fetch_work(request):
    try:
        work_id = int(request.POST[const.ViewConst.RN_WORK_ID])
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    try:
        work = models.YQWork.objects.get(pk=work_id)
    except:
        raise utils.ClientException(const.ViewConst.UNFIX)

    return {FoundationConst.RN_WORK_LIST: yiquan_utils.fit_up_work_list(work)}

# 作品页查询


# 单人完成接口
@decorators.action_render
def single_upload_work_fix(request):
    try:
        author_size = request.POST[const.ViewConst.RN_AUTHOR_SIZE]
        author_colors = request.POST[const.ViewConst.RN_AUTHOR_COLORS]
        wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
        # wx_user_openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
        worksfrontUrl = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SFRONT])
        worksbackUrl = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SBACK])
        imagefront = request.POST[const.ViewConst.RN_WORK_IMAGE_FRONT].encode(FoundationConst.ENCODE_UTF8)
        imageback = request.POST[const.ViewConst.RN_WORK_IMAGE_BACK].encode(FoundationConst.ENCODE_UTF8)
    except Exception as e:
        raise utils.ClientException(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION)

    try:
        yqwork = models.YQWork.objects.create(
            openid = wx_user_openid,
            ImageFront = imagefront,
            ImageBack = imageback,
            ImageSBack = worksbackUrl,
            ImageSFront = worksfrontUrl,
            fixstatus = 0
        )
        PrinWork = models.PrintWork.objects.create(
            size = author_size,
            colors = author_colors,
            openid = wx_user_openid,
            isprint = 1,
            printcode = None,
            workid = yqwork.id
        )
    except Exception as e:
        return HttpResponse(e)
    try:

        Code = PrinWork.id
        PrintCode = str(Code).zfill(6)
        models.PrintWork.objects.filter(size=author_size, colors=author_colors, isprint=1, workid=yqwork.id).update(printcode=PrintCode)
        return {const.ViewConst.RN_WORK_ID:yqwork.id, const.ViewConst.RN_CODE:PrintCode}
    except Exception as e:
        return HttpResponse(e)

# 单人完成接口
@decorators.action_render
def workaddcount(request):
    try:
        author_size = request.POST[const.ViewConst.RN_AUTHOR_SIZE]
        author_colors = request.POST[const.ViewConst.RN_AUTHOR_COLORS]
        wx_user_openid = "workcountadd"
        # wx_user_openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
        worksfrontUrl = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SFRONT])
        worksbackUrl = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SBACK])
        imagefront = request.POST[const.ViewConst.RN_WORK_IMAGE_FRONT].encode(FoundationConst.ENCODE_UTF8)
        imageback = request.POST[const.ViewConst.RN_WORK_IMAGE_BACK].encode(FoundationConst.ENCODE_UTF8)
    except Exception as e:
        raise utils.ClientException(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION)

    try:
        yqwork = models.YQWork.objects.create(
            openid=wx_user_openid,
            ImageFront=imagefront,
            ImageBack=imageback,
            ImageSBack=worksbackUrl,
            ImageSFront=worksfrontUrl,
            fixstatus=0
        )
        PrinWork = models.PrintWork.objects.create(
            size=author_size,
            colors=author_colors,
            openid=wx_user_openid,
            isprint=1,
            printcode=None,
            workid=yqwork.id
        )
    except Exception as e:
        return HttpResponse(e)
    try:

        Code = PrinWork.id
        PrintCode = str(Code).zfill(6)
        models.PrintWork.objects.filter(size=author_size, colors=author_colors, isprint=1,
                                        workid=yqwork.id).update(printcode=PrintCode)
        return {const.ViewConst.RN_WORK_ID: yqwork.id, const.ViewConst.RN_CODE: PrintCode}
    except Exception as e:
        return HttpResponse(e)


# 返回openid接口
@decorators.action_render
def openid(request):
    openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
    # openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
    return {const.ViewConst.RN_OPEN_ID:openid}


# 发起者提交作品接口
@decorators.action_render
def finishWork(request):
    try:
        workid = request.POST[const.ViewConst.RN_WORK_ID].encode(FoundationConst.ENCODE_UTF8)
        openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
        # openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
    except Exception as e:
        raise utils.ClientException(str(e))
    try:
        ModelWork = models.YQWork.objects.get(id=workid)
        if openid == ModelWork.openid:
            models.YQWork.objects.filter(id=workid).update(
                fixstatus=0,
            )
            return {"result_code": 0, const.ViewConst.RN_WORK_ID: workid}
        else:
            return {"result_code": 1, "msg": "不是作品发起人"}
    except Exception as e:
        return HttpResponse(e)


# 多人分享接口
@decorators.action_render
def shareupload(request):
    if int(request.POST['workId'].encode(FoundationConst.ENCODE_UTF8)) == 0:
        try:
            authsize = request.POST[const.ViewConst.RN_AUTHOR_SIZE]
            authorcolors = request.POST[const.ViewConst.RN_AUTHOR_COLORS]
            openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
            # openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
            imagesfront = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SFRONT])
            imagesback = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SBACK])
            imageback = request.POST.get(const.ViewConst.RN_WORK_IMAGE_BACK).encode(FoundationConst.ENCODE_UTF8)
            imagefront = request.POST.get(const.ViewConst.RN_WORK_IMAGE_FRONT).encode(FoundationConst.ENCODE_UTF8)
        except Exception as e:
            raise utils.ClientException(str(e))
        try:
            yqwork = models.YQWork.objects.create(
                openid = openid,
                ImageFront = imagefront,
                ImageBack = imageback,
                ImageSBack = imagesback,
                ImageSFront = imagesfront,
                fixstatus = 1
                )

            PrinWork = models.PrintWork.objects.create(
                size = authsize,
                colors = authorcolors,
                isprint = 1,
                printcode = None,
                workid = yqwork.id,
                openid = openid
            )
            Code = PrinWork.id
            PrintCode = str(Code).zfill(6)
            models.PrintWork.objects.filter(id=PrinWork.id).update(printcode=PrintCode)
            return {const.ViewConst.RN_WORK_ID: yqwork.id, const.ViewConst.RN_CODE: PrintCode, const.ViewConst.FIX_STATUS: 1}
        except Exception as e:
            return HttpResponse(e)
    else:
        try:
            workid = request.POST[const.ViewConst.RN_WORK_ID].encode(FoundationConst.ENCODE_UTF8)
            openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
            authsize = request.POST[const.ViewConst.RN_AUTHOR_SIZE]
            authorcolors = request.POST[const.ViewConst.RN_AUTHOR_COLORS]
            imagefront = json.loads(request.POST[const.ViewConst.RN_WORK_IMAGE_FRONT])
            imageback = json.loads(request.POST[const.ViewConst.RN_WORK_IMAGE_BACK])
            imagesfront = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SFRONT]).encode(FoundationConst.ENCODE_UTF8)
            imagesback = yiquan_utils.save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE_SBACK]).encode(FoundationConst.ENCODE_UTF8)
            FixstatuS = request.POST[const.ViewConst.FIX_STATUS]
        except Exception as e:
            raise utils.ClientException(str(e))
        try:
            FixStatus = models.YQWork.objects.get(id=workid)
            if FixStatus.fixstatus == "0":
                return {'isfinish':0}
            elif FixstatuS is None or FixStatus.fixstatus != int(FixstatuS):
                return {'isfinish':2}
            else:
                Fixstatus = int(FixStatus.fixstatus + 1)
                Frontimg = json.dumps(json.loads(FixStatus.ImageFront) + imagefront)
                Backimg = json.dumps(json.loads(FixStatus.ImageBack) + imageback)

                models.YQWork.objects.filter(id=workid).update(
                    ImageSFront = imagesfront,
                    ImageSBack = imagesback,
                    fixstatus = Fixstatus,
                    ImageFront = Frontimg,
                    ImageBack = Backimg
                )

                PrinWork = models.PrintWork.objects.create(
                    size = authsize,
                    colors = authorcolors,
                    openid = openid,
                    isprint = 1,
                    workid = workid,
                    printcode = None
                )
                Code = PrinWork.id
                PrintCode = str(Code).zfill(6)
                models.PrintWork.objects.filter(id=PrinWork.id).update(printcode=PrintCode)
                return {const.ViewConst.RN_WORK_ID:workid, const.ViewConst.RN_CODE:PrintCode, 'isfinish':1, const.ViewConst.FIX_STATUS: Fixstatus}
        except Exception as e:
            return HttpResponse(e)


#openid查询单个未完成
@decorators.action_render
def openidfetchs(request):
    try:
        openid = request.POST.get(const.ViewConst.RN_OPEN_ID)
        # openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
        openwork = models.YQWork.objects.filter(openid=openid, fixstatus__gt=0).first()
    except Exception as e:
        return HttpResponse(e)

    resDict = dict()
    if openwork is None:
        resDict['resultCount'] = 0
    else:
        top = models.YQWork.objects.filter(votedCount__gt=openwork.votedCount).count() + 1
        resDict['resultCount'] = 1
        resDict[const.ViewConst.RN_WORK_ID] = openwork.id
        resDict[const.ViewConst.RN_WORK_IMAGE_SFRONT] = openwork.ImageSFront.url
        resDict[const.ViewConst.RN_WORK_IMAGE_SBACK] = openwork.ImageSBack.url
        resDict[const.ViewConst.RN_VOTE] = openwork.votedCount
        resDict[const.ViewConst.FIX_STATUS] = openwork.fixstatus
        resDict[const.ViewConst.RN_TOP] = top

        # 判断打开此页面的用户是否已经参与制作过
        try:
            openid_session = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
            printWork = models.PrintWork.objects.filter(workid=openwork.id, openid=openid_session).first()
        except Exception as e:
            return HttpResponse(e)
        if printWork is None:
            resDict['isJoin'] = 0
        else:
            resDict['isJoin'] = 1
        if openid == openid_session:
            resDict["isOwner"] = 1
        else:
            resDict["isOwner"] = 0

    try:
        return resDict
    except Exception as e:
        return HttpResponse(e)




# 政哥变态需求alpha版
@decorators.action_render
def vescount(request):
    openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
    openwork = models.YQWork.objects.filter(openid=openid, fixstatus__gt=0).first()
    resDict = dict()
    if openwork is None:
        resDict['resultCount'] = 0
    else:
        resDict['resultCount'] = 1
        resDict[const.ViewConst.RN_WORK_ID] = openwork.id
        resDict[const.ViewConst.RN_WORK_IMAGE_SFRONT] = openwork.ImageSFront.url
        resDict[const.ViewConst.RN_WORK_IMAGE_SBACK] = openwork.ImageSBack.url
        resDict[const.ViewConst.RN_VOTE] = openwork.votedCount
        resDict[const.ViewConst.FIX_STATUS] = openwork.fixstatus
        resDict[const.ViewConst.RN_TOP] = 0

        # 判断打开此页面的用户是否已经参与制作过
        try:
            openid_session = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
            printWork = models.PrintWork.objects.filter(workid=openwork.id, openid=openid_session).first()
        except Exception as e:
            return HttpResponse(e)
        if printWork is None:
            resDict['isJoin'] = 0
        else:
            resDict['isJoin'] = 1
        if openid == openid_session:
            resDict["isOwner"] = 1
        else:
            resDict["isOwner"] = 0

    try:
        return resDict
    except Exception as e:
        return HttpResponse(e)

# 查询用户单个作品
@decorators.action_render
def searchwork(request):
    try:
        workid = request.POST[const.ViewConst.RN_WORK_ID].encode(FoundationConst.ENCODE_UTF8)
        openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
        # openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
        workinfo = models.YQWork.objects.filter(id=workid).first()
        WorkInfo = models.PrintWork.objects.filter(workid=workid, openid=openid).first()
        top = models.YQWork.objects.filter(votedCount__gte=workinfo.votedCount).count() + 1
    except Exception as e:
        return HttpResponse(e)

    resDict = dict()
    resDict[const.ViewConst.RN_WORK_ID] = workid
    resDict[const.ViewConst.RN_WORK_IMAGE_SFRONT] = workinfo.ImageSFront.url
    resDict[const.ViewConst.RN_WORK_IMAGE_SBACK] = workinfo.ImageSBack.url
    resDict[const.ViewConst.RN_VOTE] = workinfo.votedCount
    resDict[const.ViewConst.FIX_STATUS] = workinfo.fixstatus
    resDict[const.ViewConst.RN_TOP] = top

    resOpenid = openid
    if WorkInfo == None:
        try:
            WorkInfo = models.PrintWork.objects.filter(workid=workid, openid=workinfo.openid).first()
            resOpenid = workinfo.openid
        except Exception as e:
            return HttpResponse(e)
        resDict["isJoin"] = 0
    else:
        resDict["isJoin"] = 1

    resDict[const.ViewConst.RN_AUTHOR_SIZE] = WorkInfo.size
    resDict[const.ViewConst.RN_AUTHOR_COLORS] = WorkInfo.colors
    resDict[const.ViewConst.RN_CODE] = WorkInfo.printcode

    try:
        wx_user_info = models.WXUser.objects.filter(openid=resOpenid).first()
        nickname = wx_user_info.nickname
    except Exception as e:
        return HttpResponse(e)
    resDict[const.ViewConst.RN_NICKNAME] = nickname.encode(FoundationConst.ENCODE_UTF8)

    if openid == workinfo.openid:
        resDict["isOwner"] = 1
    else:
        resDict["isOwner"] = 0
    try:
        return resDict
    except Exception as e:
        return HttpResponse(e)


# 查询用户单个作品,提供投票
@decorators.action_render
def searchVoteWork(request):
    try:
        workid = request.POST[const.ViewConst.RN_WORK_ID].encode(FoundationConst.ENCODE_UTF8)
        # openid = "ovKICt-I4kBW4_WWrlL9uQvXLxBc"
        workinfo = models.YQWork.objects.get(id=workid)
        WorkInfo = models.PrintWork.objects.get(workid=workid, openid=workinfo.openid)
        wx_user_info = models.WXUser.objects.get(openid=workinfo.openid)
        nickname = wx_user_info.nickname
        top = models.YQWork.objects.filter(votedCount__gte=workinfo.votedCount).count() + 1
    except Exception as e:
        return HttpResponse(e)

    resDict = dict()
    resDict[const.ViewConst.RN_WORK_ID] = workid
    resDict[const.ViewConst.RN_WORK_IMAGE_SFRONT] = workinfo.ImageSFront.url
    resDict[const.ViewConst.RN_WORK_IMAGE_SBACK] = workinfo.ImageSBack.url
    resDict[const.ViewConst.RN_VOTE] = workinfo.votedCount
    resDict[const.ViewConst.RN_VOTE] = top

    resDict[const.ViewConst.RN_WORK_IMAGE_SBACK] = nickname.encode(FoundationConst.ENCODE_UTF8)

    resDict[const.ViewConst.RN_AUTHOR_SIZE] = WorkInfo.size
    resDict[const.ViewConst.RN_AUTHOR_COLORS] = WorkInfo.colors
    resDict[const.ViewConst.RN_AUTHOR_COLORS] = WorkInfo.printcode
    resDict["isJoin"] = 1

    try:
        return resDict
    except Exception as e:
        return HttpResponse(e)


# workid openid查询多个作品, 判断是否为本人
@decorators.action_render
def Workidfetchworks(request):
    try:
        openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
        workid = request.POST[const.ViewConst.RN_WORK_ID].encode(FoundationConst.ENCODE_UTF8)
        YQWORKINFO = models.YQWork.objects.get(id=workid)
    except Exception as e:
        return HttpResponse(e)

    dict_work = dict()
    WORKSINFO = models.PrintWork.objects.filter(workid=workid, openid=openid).first()
    if WORKSINFO.size:
        ModelPrintWork = WORKSINFO[0]

        dict_work['isRelation'] = 1
    else:
        try:
            ModelPrintWork = models.PrintWork.objects.get(workid=workid, openid=YQWORKINFO.openid)
        except Exception as e:
            return HttpResponse(e)
        dict_work['isRelation'] = 0

    dict_work['workId'] = workid
    dict_work[const.ViewConst.RN_WORK_IMAGE_SFRONT] = YQWORKINFO.ImageSFront.url
    dict_work[const.ViewConst.RN_WORK_IMAGE_SBACK] = YQWORKINFO.ImageSBack.url
    dict_work['workVotedCout'] = YQWORKINFO.votedCount
    dict_work['workCreationTime'] = (YQWORKINFO.creationTime + yiquan_utils.datetime.timedelta(hours=8)).strftime(FoundationConst.EXPORT_DATETIME_MINUTE_FORMAT)
    dict_work['Fix_Status'] = YQWORKINFO.fixstatus
    dict_work[const.ViewConst.RN_AUTHOR_SIZE] = ModelPrintWork.size
    dict_work[const.ViewConst.RN_AUTHOR_COLORS] = ModelPrintWork.colors
    # 查询排名
    dict_work['top'] = models.YQWork.objects.filter(votedCount__gt=YQWORKINFO.votedCount).count() + 1
    return dict_work


# workid 查询单个作品
def workidfetchwork(request):
    try:
        openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
        nickname = models.WXUser.objects.get(openid=openid)
        workid = request.POST[const.ViewConst.RN_WORK_ID].encode(FoundationConst.ENCODE_UTF8)
        YQWORKINFO = models.YQWork.objects.get(id=workid)
        worksinfo = models.PrintWork.objects.get(workid=workid, openid=YQWORKINFO.openid)
        top = models.YQWork.objects.filter(votedCount__gte=YQWORKINFO.votedCount).count() + 1
    except Exception as e:
        return HttpResponse(e)
    try:
        return {const.ViewConst.RN_AUTHOR_SIZE: worksinfo.size,
                const.ViewConst.RN_WORK_ID:workid,
                const.ViewConst.RN_CODE:worksinfo.printcode,
                const.ViewConst.RN_AUTHOR_COLORS: worksinfo.colors,
                const.ViewConst.RN_WORK_IMAGE_SFRONT: YQWORKINFO.ImageSFront.url,
                const.ViewConst.RN_WORK_IMAGE_SBACK: YQWORKINFO.ImageSBack.url,
                const.ViewConst.RN_NICKNAME: nickname.nickname,
                const.ViewConst.RN_VOTE:YQWORKINFO.votedCount,
                const.ViewConst.RN_TOP: top}
    except Exception as e:
        return HttpResponse(e)



#  OPENID查询多个作品
@decorators.action_render
def myfetchworks(request):
    try:
        openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
        # openid = "ovKICt9QiZ0gXcTKgU7caImmDCm0"
        worksinfo = models.PrintWork.objects.filter(openid=openid).all()
        worklist = yiquan_utils.fit_up_work_lists(worksinfo)
        # list_work = list()
        # for WORK in worksinfo:
        #     WORKSIMG = models.YQWork.objects.get(id=WORK.workid)
        #     dict_work = dict()
        #     dict_work['workId'] = WORK.workid
        #     dict_work['workImageSFront'] = WORKSIMG.ImageSFront.url
        #     dict_work['workImageSBack'] = WORKSIMG.ImageSBack.url
        #     dict_work['workVotedCout'] = WORKSIMG.votedCount
        #     dict_work['workCreationTime'] = (WORKSIMG.creationTime + datetime.timedelta(hours=8)).strftime(FoundationConst.EXPORT_DATETIME_MINUTE_FORMAT)
        #     dict_work['AuthorSize'] = WORK.size
        #     dict_work['AuthorColors'] = WORK.colors
        #     dict_work[const.ViewConst.RN_NICKNAME] = wx_user_info
        #     # 查询排名
        #     dict_work['top'] = models.YQWork.objects.filter(votedCount__gt=WORKSIMG.votedCount).count() + 1
        #     list_work.append(dict_work)
        return {FoundationConst.RN_WORK_LIST:worklist}
    except Exception as e:
        return HttpResponse(e)


# printcode查多个作品
@decorators.action_render
def Myfetchwork(request):
    try:
        printcode = request.POST[const.ViewConst.RN_CODE]
        worksinfo = models.PrintWork.objects.get(printcode=printcode)
        WORK = models.YQWork.objects.get(id=worksinfo.workid)
        dict_work = dict()
        dict_work['workId'] = WORK.workid
        dict_work['workImageSFront'] = WORK.ImageSFront.url
        dict_work['workImageSBack'] = WORK.ImageSBack.url
        dict_work['workCreationTime'] = (WORK.creationTime + yiquan_utils.datetime.timedelta(hours=8)).strftime(FoundationConst.EXPORT_DATETIME_MINUTE_FORMAT)
        dict_work['AuthorSize'] = worksinfo.size
        dict_work['AuthorColors'] = worksinfo.colors
        # 查询排名
        dict_work['top'] = models.YQWork.objects.filter(votedCount__gt=WORK.votedCount).count() + 1
        list_work = list()
        list_work.append(dict_work)
        return {FoundationConst.RN_WORK_LIST:list_work}
    except Exception as e:
        return HttpResponse(e)


@decorators.action_render
def openidfetch(request):
    openid = request.session[FoundationConst.PLATFORM_WEIXIN_OPENID]
    Work = models.YQWork.objects.filter(openid=openid)
    return {const.ViewConst.RN_WORK_ID:Work.id}


@decorators.action_render
def pc_vote(request):
    try:
         work_id = int(request.POST['workId'])
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    ip = utils.get_ip_from_request(request)
    wx_user = None
    wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_OPENID)
    if wx_user_openid is None:
        pass
    else:
        wx_user = models.WXUser.objects.filter(openid=wx_user_openid).first()

    vote_manager = YiQuanVoteManager()
    vote_manager.vote(work_id, wx_user=wx_user, ip=ip)


@decorators.action_render
def get_sign_package(request):
    try:
        url = request.POST['url']
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    sign_package = wechat_api.wechatAPI.get_sign_package(url)
    return sign_package


@decorators.action_render
def addtest(request):
    try:
        openid = "123klajs"
        printcode = '231312'
        isprint = FoundationConst.PRINT
        workid = 1
        test = models.PrintWork.objects.create(
            openid = openid,
            printcode = printcode,
            isprint = isprint,
            workid = workid
        )
        return HttpResponse("SUCCESS")
    except Exception as e:
        return HttpResponse(e)



@decorators.action_render
def fetch_front_image_func(request):
    workid = request.GET[const.ViewConst.RN_WORK_ID]
    imageinfo = models.YQWork.objects.get(pk=workid)
    feature_list = json.loads(imageinfo.ImageFront)
    front_image_filename = regenerate.regenerate(feature_list)
    return utils.file_for_download(front_image_filename, const.WorkConst.SHOW_NAME_FRONT_IMAGE)


@decorators.action_render
def fetch_back_image_func(request):
    workid = request.GET[const.ViewConst.RN_WORK_ID]
    imageinfo = models.YQWork.objects.get(pk=workid)
    feature_list = json.loads(imageinfo.ImageBack)
    back_image_filename = regenerate.regenerate(feature_list)
    return utils.file_for_download(back_image_filename, const.WorkConst.SHOW_NAME_BACK_IMAGE)