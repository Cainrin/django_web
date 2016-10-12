# -*- coding: utf-8 -*-
from campaigns.foundation.applet.vote import VoteManager
from campaigns.yh.models import Vote, Work, WXUser
from campaigns.yh.config import VoteConfig
from campaigns.yh import app_id


class FendaVoteManager(VoteManager):
    def __init__(self):
        super(FendaVoteManager, self).__init__(
            app_id=app_id,
            work_class=Work,
            vote_class=Vote,
            wx_user_class=WXUser,
            ip_limit_count=VoteConfig.IP_LIMIT_COUNT,
            weixin_limit_count=VoteConfig.WEIXIN_LIMIT_COUNT
        )

