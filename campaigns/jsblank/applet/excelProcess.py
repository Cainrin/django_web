# -*- encoding: utf-8 -*-
import multiprocessing, time
from django.db import connection


class ExcelProcess(multiprocessing.Process):
    def __init__(self):
        self.result_resason = None
        super(ExcelProcess, self).__init__()

    def run(self):
        try:
            connection.connection.close()
            connection.connection = None
        except:
            print 111
        self.beginning()
        self.drawExcel()
        self.cheat_finished()


    def cheat_finished(self):
        pass

    def drawExcel(self):
        pass

    def beginning(self):
        pass