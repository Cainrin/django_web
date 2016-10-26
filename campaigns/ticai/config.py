# -*- coding: utf-8 -*-
import time

class WorkConfig(object):
    # relative path
    REL_PATH_IMAGE = 'campaigns/ticai/work/image/'
    starTime = time.mktime(time.strptime("2016-10-26", "%Y-%m-%d"))
    week = 1

class VoteConfig(object):
    IP_LIMIT_COUNT = 3
    WEIXIN_LIMIT_COUNT = 3


class ViewConfig(object):
    STATIC_URL = 'campaigns/ticai/'
    TEMPLATE_URL = 'ticai/'
    TEMPLATE_PC_URL = TEMPLATE_URL + 'pc/'
    TEMPLATE_MOBILE_URL = TEMPLATE_URL + 'mobile/'