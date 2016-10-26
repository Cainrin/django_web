# -*- coding: utf-8 -*-
from django.conf import settings
import redis
from campaigns.foundation.const import FoundationConst


def redis_session(name=FoundationConst.VN_DEFAULT, index=0):
    info = None
    if name is not None:
        info = settings.REDIS[name]
    elif index is not None:
        info = settings.REDIS.values()[index]
    return redis.StrictRedis(info[FoundationConst.REDIS_HOST], info[FoundationConst.REDIS_PORT], info[FoundationConst.REDIS_INDEX], info[FoundationConst.REDIS_PASSWORD])
