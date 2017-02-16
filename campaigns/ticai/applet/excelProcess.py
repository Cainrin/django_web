# -*- encoding: utf-8 -*-
import multiprocessing, time
from django.db import connection
from campaigns.ticai.applet import walkExcel


class ExcelProcess(multiprocessing.Process):
    def __init__(self):
        self.result_resason = None
        super(ExcelProcess, self).__init__()

    def run(self):
        connection.connection.close()
        connection.connection = None
        self.beginning()
        self.drawExcel()
        self.cheat_finished()


    def cheat_finished(self):
        pass

    def drawExcel(self):
        pass

    def beginning(self):
        pass