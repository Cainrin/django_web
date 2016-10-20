# -*- coding: utf-8 -*-
import random
from campaigns.foundation.applet import cheat
from campaigns.foundation.const import FoundationConst
from campaigns.hypro import const, models


class VoteCheatProcess(cheat.CheatProcess):
    def __init__(self, vote_cheat):
        self.vote_cheat = vote_cheat
        if self.vote_cheat.type == const.VoteCheatConst.TYPE_ONE:
            self.work_id_list = [self.vote_cheat.work.id for x in xrange(self.vote_cheat.totalCount)]
        else:
            total_id_list = models.Work.objects.values_list('id', flat=True).filter(status=FoundationConst.STATUS_ONLINE)
            if 201 in total_id_list:
                total_id_list = list(total_id_list)
                total_id_list.remove(201)
            if 202 in total_id_list:
                total_id_list = list(total_id_list)
                total_id_list.remove(202)
            self.work_id_list = [random.choice(total_id_list) for x in xrange(self.vote_cheat.totalCount)]
        interval_seconds = float(self.vote_cheat.minute) * 60 / float(self.vote_cheat.totalCount)
        super(VoteCheatProcess, self).__init__(interval_seconds, self.vote_cheat.totalCount)

    def cheat(self):
        work = models.Work.objects.get(pk=self.work_id_list[self.now_count])
        # 当刷票进行时，此作品被删除，才会出现为None情况
        if work is None:
            return
        models.Vote.objects.create(
            work=work,
            platform=FoundationConst.PLATFORM_DESKTOP,
            ip=self.vote_cheat.ip,
            status=FoundationConst.STATUS_ONLINE
        )
        self.vote_cheat.nowCount += 1
        self.vote_cheat.save()

    def cheat_finished(self):
        self.vote_cheat.hasFinished = True
        self.vote_cheat.save()

