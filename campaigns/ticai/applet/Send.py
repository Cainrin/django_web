# -*- coding: utf-8 -*-
import multiprocessing, time
from django.db import connection


class CheatProcess(multiprocessing.Process):
    def __init__(self, interval_seconds, total_count):
        self.interval_seconds = interval_seconds
        self.total_count = total_count
        self.result_reason = None
        self.now_count = 0
        super(CheatProcess, self).__init__()

    def run(self):
        connection.connection.close()
        connection.connection = None
        while True:
            start_seconds = time.time()
            a = self.cheat()
            if a == False:
                break
            self.now_count += 1
            if not self._can_continue_to_cheat():
                self.result_reason = "已发完"
                break
            end_seconds = time.time()
            delta_seconds = end_seconds - start_seconds
            if delta_seconds < self.interval_seconds:
                time.sleep(self.interval_seconds - delta_seconds)
        self.cheat_finished()

    def _can_continue_to_cheat(self):
        return self.now_count < self.total_count

    def cheat_finished(self):
        pass

    def cheat(self):
        pass
