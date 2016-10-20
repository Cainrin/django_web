# -*- coding: utf-8 -*-
import time

class WorkConfig(object):
    # relative path
    REL_PATH_IMAGE = 'campaigns/testticai/work/image/'
    starTime = time.mktime(time.strptime("2016-10-19", "%Y-%m-%d"))
    week = 1

class VoteConfig(object):
    IP_LIMIT_COUNT = 3
    WEIXIN_LIMIT_COUNT = 3


class ViewConfig(object):
    STATIC_URL = 'campaigns/testticai/'
    TEMPLATE_URL = 'testticai/'
    TEMPLATE_PC_URL = TEMPLATE_URL + 'pc/'
    TEMPLATE_MOBILE_URL = TEMPLATE_URL + 'mobile/'