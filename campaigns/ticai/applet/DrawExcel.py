# -*- encoding: utf-8 -*-
import random, datetime, pytz
from campaigns.ticai import config
from django.utils import timezone
from campaigns.ticai.applet import walkExcel
import excelProcess
from campaigns.foundation.const import FoundationConst
from campaigns.ticai import const, models


class DrawExcelProcess(excelProcess.ExcelProcess):
    def __init__(self, vote_cheat):
        self.vote_cheat = vote_cheat
        self.result_reason = None
        super(DrawExcelProcess, self).__init__()

    def drawExcel(self):
        excel = walkExcel.countDay().startDraw()
        self.vote_cheat.excelUrl = excel
        self.vote_cheat.save()


    def cheat_finished(self):
        self.vote_cheat.hasFinished = True
        self.vote_cheat.save()

    def beginning(self):
        self.vote_cheat.hasFinished = False
        self.vote_cheat.save()