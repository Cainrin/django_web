# -*- coding: utf-8 -*-


class WXUserConst(object):
    # verbose name
    VN_TABLE_NAME = u'微信用户'


class AuthorConst(object):
    # verbose name
    VN_TABLE_NAME = u'作者信息'


class WorkConst(object):
    # verbose name
    VN_TABLE_NAME = u'作品信息'
    TYPE_PHOTO = 0
    TYPE_DIY = 10
    TYPE_CHOICES = (
        (TYPE_PHOTO, '拍照上传'),
        (TYPE_DIY, '线上制作'),
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




