# -*- coding: utf-8 -*-


class AddCode(object):
    VN_TABLE_NAME = u'增加奖卷'
    RN_TABLE_NAME = u'奖卷池'

class PricHome(object):
    VN_TABLE_NAME = u'中奖信息'


class UserPhonecallConst(object):
    VN_TABLE_NAME = u'用户信息表'


class ActiveDataConst(object):
    VN_TABLE_NAME = u'活动信息'



class PricesConst(object):
    # verbose name
    VN_TABLE_NAME = u'奖品设置'


class Lottery(object):
    # verbose name
    VN_TABLE_NAME = u'抽奖设置'


class WXUserConst(object):
    # verbose name
    VN_TABLE_NAME = u'微信用户'


class AuthorConst(object):
    # verbose name
    VN_TABLE_NAME = u'作者信息'


class WorkConst(object):
    # verbose name
    VN_TABLE_NAME = u'作品信息'
    is_send = 0
    no_send = 1
    send_choice = (
        (is_send, '已发'),
        (no_send, '未发'),
    )
    TYPE_PHOTO = 0
    TYPE_DIY = 10
    TYPE_CHOICES = (
        (TYPE_PHOTO, '拍照上传'),
        (TYPE_DIY, '线上制作'),
    )
    IS_FINISH = 0
    NO_FINISH = 1
    FINISH_CHOICES = (
        (IS_FINISH, '已完成'),
        (NO_FINISH, '未完成')
    )
    # short_description
    SD_IMAGE_TAG = '作品预览'


class ShareConst(object):
    # verbose name
    VN_TABLE_NAME = u'分享记录'


class VoteConst(object):
    # verbose name
    VN_TABLE_NAME = u'投票记录'


class VoteCheatConst(object):
    # verbose name
    VN_TABLE_NAME = u'刷票任务'
    TYPE_ALL = 0
    TYPE_ONE = 10
    TYPE_CHOICES = (
        (TYPE_ALL, '全体刷票'),
        (TYPE_ONE, '单个作品刷票'),
    )


class PageViewConst(object):
    # verbose name
    VN_TABLE_NAME = u'PV'


class UniqueVisitorConst(object):
    # verbose name
    VN_TABLE_NAME = u'UV'


class ViewConst(object):
    RN_AUTHOR_NAME = 'authorName'
    RN_AUTHOR_CELLPHONE = 'authorCellphone'
    RN_AUTHOR_SCHOOL = 'authorSchool'
    RN_WORK_NAME = 'workName'
    RN_WORK_IMAGE = 'workImage'
    RN_WORK_ID = 'workId'
    RN_WORK = 'work'
    CLIENT_EXCEPTION_WORK_IS_NONE = '此作品不存在'
    CLIENT_EXCEPTION_WORK_BANNED = '此作品已经被封禁'




