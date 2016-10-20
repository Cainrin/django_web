# -*- coding: utf-8 -*-


class WorkConfig(object):
    # relative path
    REL_PATH_IMAGE = 'campaigns/hypro/work/image/'


class VoteConfig(object):
    IP_LIMIT_COUNT = 3
    WEIXIN_LIMIT_COUNT = 3


class ViewConfig(object):
    STATIC_URL = 'campaigns/hypro/'
    TEMPLATE_URL = 'hypro/'
    TEMPLATE_PC_URL = TEMPLATE_URL + 'pc/'
    TEMPLATE_MOBILE_URL = TEMPLATE_URL + 'mobile/'
