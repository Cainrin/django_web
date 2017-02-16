# -*- coding: utf-8 -*-
import math
from campaigns.foundation.applet import response, utils
from campaigns.foundation.const import FoundationConst, DisplayConst
from campaigns.fenda201605 import models, config, const
from campaigns.foundation import wechat_api
from campaigns.fenda201605.applet import decorators
from campaigns.fenda201605.applet.vote import FendaVoteManager
from campaigns.fenda201605.applet.uitls import fit_up_work_list, save_work_image, fit_up_work
from campaigns.foundation.applet import cos


@decorators.action_render
def pc_upload_photo_work(request):
    try:
        author_name = request.POST[const.ViewConst.RN_AUTHOR_NAME].encode(FoundationConst.ENCODE_UTF8)
        author_cellphone = request.POST[const.ViewConst.RN_AUTHOR_CELLPHONE].encode(FoundationConst.ENCODE_UTF8)
        author_school = request.POST[const.ViewConst.RN_AUTHOR_SCHOOL].encode(FoundationConst.ENCODE_UTF8)
        work_name = request.POST[const.ViewConst.RN_WORK_NAME].encode(FoundationConst.ENCODE_UTF8)
        work_image_url = save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE])
    except Exception as e:
        raise utils.ClientException(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION)
    author = models.Author.objects.create(
        uuid=utils.generate_uuid(),
        name=author_name,
        cellphone=author_cellphone,
        school=author_school,
        platform=FoundationConst.PLATFORM_DESKTOP,
        ip=utils.get_ip_from_request(request)
    )
    work = models.Work.objects.create(
        name=work_name,
        image=work_image_url,
        author=author,
        type=const.WorkConst.TYPE_PHOTO,
        status=FoundationConst.STATUS_ONLINE
    )
    return {const.ViewConst.RN_WORK_ID: work.id}


@decorators.action_render
def pc_upload_diy_work(request):
    try:
        author_name = request.POST[const.ViewConst.RN_AUTHOR_NAME].encode(FoundationConst.ENCODE_UTF8)
        author_cellphone = request.POST[const.ViewConst.RN_AUTHOR_CELLPHONE].encode(FoundationConst.ENCODE_UTF8)
        author_school = request.POST[const.ViewConst.RN_AUTHOR_SCHOOL].encode(FoundationConst.ENCODE_UTF8)
        work_name = request.POST[const.ViewConst.RN_WORK_NAME].encode(FoundationConst.ENCODE_UTF8)
        work_image_url = save_work_image(request.FILES[const.ViewConst.RN_WORK_IMAGE])
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    author = models.Author.objects.create(
        uuid=utils.generate_uuid(),
        name=author_name,
        cellphone=author_cellphone,
        school=author_school,
        platform=FoundationConst.PLATFORM_DESKTOP,
        ip=utils.get_ip_from_request(request)
    )
    work = models.Work.objects.create(
        name=work_name,
        image=work_image_url,
        author=author,
        type=const.WorkConst.TYPE_DIY,
        status=FoundationConst.STATUS_ONLINE
    )
    #  上传云存储空间
    upload = cos.TxCos()
    image_path = '/www/project/cmp/media/%s' % \
                 work.image

    upload.upload_file(image_path, work.image)

    return {const.ViewConst.RN_WORK_ID: work.id}


@decorators.action_render
def pc_vote(request):
    try:
         work_id = int(request.POST['workId'])
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    ip = utils.get_ip_from_request(request)
    if work_id == 201 or work_id == 202:
        raise utils.ClientException(DisplayConst.EXCEPTION_VOTE_CAMPAIGN_HAS_PASED)
    else:
        # 尝试获取微信用户信息，如果是微信用户，则按照openid计算投票次数
        wx_user = None
        wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_NAME)
        if wx_user_openid is None:
            pass
        else:
            wx_user = models.WXUser.objects.filter(openid=wx_user_openid).first()

        vote_manager = FendaVoteManager()
        vote_manager.vote(work_id, wx_user=wx_user, ip=ip)


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
            pk_work = models.Work.objects.get(pk=maybe_id)
        except:
            pass
        total_count = models.Work.objects.filter(status=FoundationConst.STATUS_ONLINE).filter(name__contains=search_key_words).count()
        total_pages = int(math.ceil(float(total_count) / float(page_rows)))
        start = (now_page - 1) * page_rows
        end = start + page_rows
        work_list = models.Work.objects.filter(status=FoundationConst.STATUS_ONLINE).filter(name__contains=search_key_words).all()[start: end]
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
        total_count = models.Work.objects.filter(status=FoundationConst.STATUS_ONLINE).order_by(order_key).count()
        total_pages = int(math.ceil(float(total_count) / float(page_rows)))
        start = (now_page - 1) * page_rows
        end = start + page_rows
        work_list = models.Work.objects.filter(status=FoundationConst.STATUS_ONLINE).order_by(order_key).all()[start: end]
    work_list = fit_up_work_list(work_list)
    return {
        FoundationConst.RN_TOTAL_PAGES: total_pages,
        FoundationConst.RN_WORK_LIST: work_list
    }


@decorators.action_render
def pc_fetch_work(request):
    try:
        work_id = int(request.POST[const.ViewConst.RN_WORK_ID])
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    try:
        work = models.Work.objects.get(pk=work_id)
    except:
        raise utils.ClientException(const.ViewConst.CLIENT_EXCEPTION_WORK_IS_NONE)
    if work.status == FoundationConst.STATUS_BANNED:
        raise utils.ClientException(const.ViewConst.CLIENT_EXCEPTION_WORK_BANNED)
    return {const.ViewConst.RN_WORK: fit_up_work(work)}


@decorators.action_render
def get_sign_package(request):
    try:
        url = request.POST['url']
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    sign_package = wechat_api.WechatApi().get_sign_package(url)
    return sign_package


@decorators.action_render
def mobile_share(request):
    wx_user_openid = request.session.get(FoundationConst.PLATFORM_WEIXIN_NAME)
    # wx_user_openid = 'ovKICtx17dDCj-bnFqf8li6Yq_L4'
    if wx_user_openid is None:
        return {'result': 'there is no openId'}
    else:
        wx_user = models.WXUser.objects.filter(openid=wx_user_openid).first()
        if wx_user is None:
            return {'result': 'there is no WXUser'}
    try:
        url = request.POST['url']
        work_id = request.POST.get(const.ViewConst.RN_WORK_ID, None)
    except Exception as e:
        raise utils.ClientException('{0}:{1}'.format(DisplayConst.EXCEPTION_CLIENT_INCOMPLETE_INFORMATION, str(e)))
    work = None
    if work_id is not None:
        work_id = int(work_id)
        work = models.Work.objects.get(pk=work_id)
    ip = utils.get_ip_from_request(request)
    share = models.Share.objects.create(
        url=url,
        work=work,
        platform=FoundationConst.PLATFORM_WEIXIN,
        ip=ip,
        wxUser=wx_user,
    )
    return {'result': 'success'}


@decorators.action_render
def upload_test(request):
    upload = cos.TxCos()
    test = upload.upload_file("D:/DjangoCode/njhy/cmp/media/campaigns/fenda201605/work/image/5a52d0072d3f42b192a592a4cd56e2bc.png", "campaigns/fenda201605/work/image/5a52d0072d3f42b192a592a4cd56e2bc.png")
    up = 'http://huayang-10030008.file.myqcloud.com/campaigns/fenda201605/work/image/5a52d0072d3f42b192a592a4cd56e2bc.png'
    return test
