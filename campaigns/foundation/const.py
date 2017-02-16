# -*- coding: utf-8 -*-


# 普通用户可见
class DisplayConst(object):
    # common
    EXCEPTION_CLIENT_INCOMPLETE_INFORMATION = '信息不完整'
    EXCEPTION_SERVER_NOT_STD_BEHAVIOUR = '服务端程序未按标准编写'
    # vote
    EXCEPTION_VOTE_CANNOT_FETCH_CAMPAIGN_INFO = '无法获取活动配置信息'
    EXCEPTION_VOTE_CANNOT_FETCH_WORK_INFO = '无法获取作品信息'
    EXCEPTION_VOTE_CAMPAIGN_HAS_PASED = '活动因太过火爆暂停投票，稍后继续'
    EXCEPTION_VOTE_CAMPAIGN_STILL_WAITING = '活动暂未开始，请等活动开始后再来吧'
    EXCEPTION_VOTE_CAMPAIGN_HAS_FINISHED = '活动已经结束了'
    EXCEPTION_VOTE_PLATFORM_IP = '桌面平台下，请记录IP地址'
    EXCEPTION_VOTE_PLATFORM_WEIXIN = '微信平台下，请记录微信用户ID'
    EXCEPTION_AUTH_CODE_WEIXIN = '微信授权异常'
    EXCEPTION_AUTH_OPENID_WEIXIN = '获取用户信息异常'
    # page
    PAGE_400 = ''
    PAGE_403 = ''
    PAGE_404 = ''
    PAGE_500 = ''
    PAGE_501 = ''
    # action
    CONTENT_TYPE_JSON = "application/json"
    ERROR_MESSAGE = "errorMessage"
    DEFAULT_400_ERROR_MESSAGE = '错误的请求'
    DEFAULT_500_ERROR_MESSAGE = '服务端出现错误'
    DEFAULT_501_ERROR_MESSAGE = '服务端出现未知错误'


class FoundationConst(object):
    # RN_NAME
    RN_CAMPAIGNS = 'campaigns'
    RN_URL = 'url'
    RN_CREATION_TIME = 'creationTime'
    RN_IP = 'ip'
    RN_RCODE = 'result_code'
    RN_RMSG = 'result_msg'
    RN_PLATFORM = 'platform'
    RN_STATIC_URL = 'static_url'
    RN_WEIXIN_DEBUG = 'weixin_debug'
    RN_AUTHOR_UUID = 'author_uuid'
    RN_TOTAL_COUNT = 'totalCount'
    RN_TOTAL_PAGES = 'totalPages'
    RN_NOW_PAGE = 'nowPage'
    RN_WORK_LIST = 'workList'
    RN_COOKIE_LIST = 'cookie_list'
    RN_REQUEST_CUSTOM = 'CUSTOM'
    # VN_NAME
    VN_NAME = u'名称'
    VN_STRING = u'梦想'
    VN_NICKNAME = u'昵称'
    VN_PV = u'pv'
    VN_UV = u'uv'
    VN_FAKEPV = u'添加pv'
    VN_FAKEUV = u'添加uv'
    VN_QUANTITY = u'数量'
    VN_REDATE = u'活动时间'
    VN_DONE = u'领取状态'
    VN_UCOUNT = u'单个用户抽奖次数'
    VN_DCOUNT = u'每天抽奖次数'
    VN_STARTIME = u'起始时间'
    VN_STOPTIME = u'结束时间'
    VN_PRIZES = u'奖品'
    VN_ACTIVEID = u'活动ID'
    VN_ACTIVENAME = u'活动名称'
    VN_USRINFO = u'用户信息'
    VN_CHANCE = u'中奖几率'
    VN_FICHANCE = u'虚拟实物几率'
    VN_PRINAME = u'详细奖品名称'
    VN_ACTIME = u'步数上传时间'
    VN_PRITYPE = u'奖品类型'
    VN_PRIMON = u'奖品金额'
    VN_PRICOUNT = u'奖品数量'
    VN_SEND = u'已发奖品'
    VN_COMMENT = u'备注'
    VN_USER = u'中奖人'
    VN_USRTIME = u'session'
    VN_CELLPHONE = u'手机号'
    VN_SCHOOL = u'院校'
    VN_CITY = u'城市'
    VN_ISDOLE = u'是否被领取'
    VN_GENDER = u'性别'
    VN_SIZE = u'尺码'
    VN_ID = u'编号'
    VN_USRID = u'用户ID'
    VN_FRONBACK = u'正反面'
    VN_COLORS = u'颜色'
    VN_FIX = u'已完成'
    VN_PHONENU = u'手机号'
    VN_PRINUM = u'奖品编号'
    VN_ADDRESS = u'住址'
    VN_DOLE = u'领取状况'
    VN_PRINT = u'打印状态'
    VN_PRINTID = u'打印碼'
    VN_STATUS = u'状态'
    VN_MON = u'总金额'
    SD_MON = u'已发金额'
    VN_CMON = u'步数金额'
    VN_PMON = u'抽奖金额'
    VN_PLATFORM = u'平台类型'
    VN_CREATION_TIME = u'创建时间'
    VN_DateTime = u'点亮时间'
    VN_MANIC = u'中奖几率'
    VN_PROSEN = u'活动人数'
    VN_UPDATE_TIME = u'更新时间'
    VN_SIGNTIME = u'线下活动时间'
    VN_SIGNUSR = u'线下活动用户信息'
    VN_PRITIME = u'中奖时间'
    VN_USRPRI = u'中奖用户'
    VN_IP = u'IP地址'
    VN_IMAGE = u'图片'
    VN_BCOUNT = u'步数'
    VN_CBCOUNT = u'更改步数'
    VN_FRONT = u'正面'
    VN_BACK = u'背面'
    VN_WORKCOUNT = u'刷作品数量'
    VN_SFRONT = u'小正'
    VN_SBACK = u'小反'
    VN_TYPE = u'类型'
    VN_SHARED_COUNT = u'分享次数'
    VN_VOTED_COUNT = u'获得投票数'
    VN_URL = u'链接'
    VN_COUNT = u'数量'
    VN_TOTAL_COUNT = u'总量'
    VN_NOW_COUNT = u'现在的量'
    VN_HAS_FINISHED = u'已经完成'
    VN_MINUTE = u'花费时间（分钟）'
    # gender
    GENDER_PRIVATE = 0
    GENDER_MALE = 10
    GENDER_FEMALE = 20
    GENDER_CHOICES = (
        (GENDER_PRIVATE, '保密'),
        (GENDER_MALE, '男性'),
        (GENDER_FEMALE, '女性'),
    )

    SINGLE = 0
    ALL = 1
    EXPORT_CHOICE = (
        (SINGLE, '前一天参数'),
        (ALL, '所有参数')
    )

    read = 0
    unread = 1
    READ_CHOICES = (
        (read, '已读'),
        (unread, '未读')
    )


    XN = 0
    SW = 1
    TYPE_CHOICES = (
        (XN, '虚拟'),
        (SW, '实物')
    )


    #ISPRINT
    PRINT = 0
    UNPRINT = 1
    PRINT_CHOICES = (
        (PRINT, '已打印'),
        (UNPRINT, '未打印')
    )
    #FRONBACK
    FRONT = 0
    BACK = 1
    FRONBACK_CHOICES = (
        (FRONT, '正面'),
        (BACK, '反面')
    )
    # 奖品
    MISS = 0
    FIRST = 1
    SEC = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10
    EVENTH = 11
    TWELEVTH = 12
    THIRTEENTH = 13
    FOURTEENTH = 14
    FIFTEENTH = 15
    PRIZES_CHOICES = (
        (FIRST, '一等奖'),
        (SEC, '二等奖'),
        (THIRD, '三等奖'),
        (FOURTH, '四等奖'),
        (FIFTH, '五等奖'),
        (SIXTH, '六等奖'),
        (SEVENTH, '七等奖'),
        (EIGHTH, '八等奖'),
        (NINTH, '九等奖'),
        (TENTH, '十等奖'),
        (MISS, '谢谢参与')
    )
    WEEK = 0
    DAY = 1
    MAX = 2
    COUNT_CHOICES = (
        (WEEK, '周排名'),
        (DAY, '日排名'),
        (MAX, '总排名')
    )
    #size
    SIZES = 0
    SIZEM = 1
    SIZEL = 2
    SIZEXL = 3
    SIZE_CHOICES = (
        (SIZES, 'S尺寸'),
        (SIZEM, 'M尺寸'),
        (SIZEL, 'L尺寸'),
        (SIZEXL, 'XL尺寸')
    )
    IS_SEND = 0
    NO_SEND = 1
    SEND_CHOICES = (
        (IS_SEND, "已发"),
        (NO_SEND, "未发")
    )
    TRUE = 0
    FALSE = 1
    LT_CHOICE = (
        (TRUE, '联通'),
        (FALSE, '其他')
    )

    #colors
    black = 0
    white = 3
    green = 2
    yellow = 1
    COLOR_CHOICES = (
        (black, '黑色'),
        (white, '白色'),
        (green, '绿色'),
        (yellow, '黄色')
    )
    # FIX_STATUS
    UNFIX = 1
    FIX = 0
    FIX_STATUS_CHOICES = (
        (UNFIX, '未完成'),
        (FIX, '已完成')
    )

    golden = 1
    silver = 0
    IPHONE = 2
    PEAS_CHOICES = (
        (golden, '金豆子'),
        (silver, '银豆子'),
        (IPHONE, 'iphone')
    )

    # 是否领取
    DOLE = 0
    UNDOLE = 1
    IS_DOLE_CHOICES = (
        (DOLE, '已中奖'),
        (UNDOLE, '未中奖')
    )

    DONE = 0
    UNDONE = 1
    IS_DONE_CHOICES = (
        (DONE, '已领取'),
        (UNDONE, '未领取')
    )

    # common status
    STATUS_WAITING = 0
    STATUS_ONLINE = 10
    STATUS_BANNED = 20
    STATUS_CHOICES = (
        (STATUS_WAITING, '等待审核'),
        (STATUS_ONLINE, '正常'),
        (STATUS_BANNED, '封禁'),
    )
    # platform
    VN_DESKTOP = u'桌面'
    VN_WEIXIN = u'微信'
    VN_WEIBO = u'微博'
    VN_QQ = u'QQ'
    PLATFORM_IP_NAME = 'ip'
    PLATFORM_WEIXIN_NAME = 'wxUser'
    PLATFORM_WEIXIN_OPENID = 'openid'
    PLATFORM_AUTH_STATE = 'authState'
    PLATFORM_WEIBO_NAME = 'wbUser'
    PLATFORM_QQ_NAME = 'qqUser'
    PLATFORM_DESKTOP = 0
    PLATFORM_WEIXIN = 10
    PLATFORM_WEIBO = 20
    PLATFORM_QQ = 30
    PLATFORM_CHOICES = (
        (PLATFORM_DESKTOP, VN_DESKTOP),
        (PLATFORM_WEIXIN, VN_WEIXIN),
        # (PLATFORM_WEIBO, VN_WEIBO),
        # (PLATFORM_QQ, VN_QQ)
    )
    # tag
    TAG_LIST_DISPLAY_IMAGE = '<img class="list_display_img fancybox" data-fancybox-group="gallery" href="{0}" src="{0}">'
    # action
    ACTION_EXPORT_EXCEL = '导出到Excel文件'
    # default
    DEFAULT_IP = u"0.0.0.0"
    # exception
    EXCEPTION_PLATFORM_IP = '桌面平台下，请录入IP地址'
    EXCEPTION_PLATFORM_WEIXIN = '微信平台下，请录入微信用户'
    # export
    EXPORT_EXCEL_STYLE = u"align: horizontal center;"
    EXPORT_DATETIME_SECOND_FORMAT = "%Y年%m月%d %H:%M:%S"
    EXPORT_DATETIME_MINUTE_FORMAT = "%Y年%m月%d %H:%M"
    EXPORT_BOOL_TRUE = u"是"
    EXPORT_BOOL_FALSE = u"否"
    # ENCODE
    ENCODE_UTF8 = 'utf-8'
    # common name
    VN_DEFAULT = u'default'
    REDIS_HOST = 'HOST'
    REDIS_PORT = 'PORT'
    REDIS_INDEX = 'INDEX'
    REDIS_PASSWORD = 'PASSWORD'
    # redis
    REDIS_LIST_PV = 'pv'
    REDIS_LIST_UV = 'uv'
    # qcloud_cos
    QCLOUD_COS_APP_ID = 'APP_ID'
    QCLOUD_COS_SECRET_ID = 'SECRET_ID'
    QCLOUD_COS_SECRET_KEY = 'SECRET_KEY'
    QCLOUD_COS_BUCKET = 'BUCKET'
    QCLOUD_COS_EXCEPTION_UPLOAD_FAILED = '文件上传失败'
    RN_CODE = 'code'
    RN_MESSAGE = 'message'
    # django
    DJANGO_HTTP_X_FORWARDED_FOR = 'HTTP_X_FORWARDED_FOR'
    DJANGO_REMOTE_ADDR = 'REMOTE_ADDR'
    DJANGO_HTTP_USER_AGENT = 'HTTP_USER_AGENT'
    # identity
    IDENTITY_WEIXIN = 'MicroMessenger'
    # regenerate
    RN_CANVAS = 'canvas'
    RN_KIT_LIST = 'kitList'
    RN_ZOOM = 'zoom'
    RN_RGBA = 'RGBA'
    RN_WIDTH = 'width'
    RN_HEIGHT = 'height'
    RN_INDEX = 'index'
    RN_X = 'x'
    RN_Y = 'y'
    RN_SCALE = 'scale'
    RN_ANGLE = 'angle'


class CampaignConst(object):
    # verbose name
    VN_TABLE_NAME = u'活动信息'
    VN_NAME = u'名称'
    VN_INTRO = u'描述'
    VN_APP_NAME = u'应用名称'
    VN_STATUS = u'状态'
    VN_HAS_PAUSED = u'是否暂停'
    VN_START_TIME = u'开始时间'
    VN_END_TIME = u'结束时间'
    VN_CREATION_TIME = u'创建时间'
    # status
    STATUS_WAITING = 0
    STATUS_ONLINE = 10
    STATUS_FINISHED = 20
    STATUS_CHOICES = (
        (STATUS_WAITING, '等待上线'),
        (STATUS_ONLINE, '上线中'),
        (STATUS_FINISHED, '已经结束'),
    )
    # fieldsets
    FIELDSETS_BASIC = '基本信息'
    FIELDSETS_KEY = '程序调用的关键信息'
    FIELDSETS_ADDITION = '补充信息'


class WeixinConst(object):
    VN_TABLE_NAME = u'微信公众号'
    VN_NAME = u'名称'
    VN_KEY = u'Key'
    VN_SECRET = u'Secret'
    VN_Token = u'Token'
    VN_EncodingAESKey = u'EncodingAESKey'
    VN_UPDATE_TIME = u'上次修改'
    VN_CREATION_TIME = u'创建时间'
