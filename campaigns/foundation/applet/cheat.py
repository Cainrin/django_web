# -*- coding: utf-8 -*-
import multiprocessing, time
from django.db import close_old_connections, connection


class CheatProcess(multiprocessing.Process):
    def __init__(self, interval_seconds, total_count):
        self.interval_seconds = interval_seconds
        self.total_count = total_count
        self.now_count = 0
        super(CheatProcess, self).__init__()

    def run(self):
        try:
            connection.connection.close()
            connection.connection = None
        except:
            print 111
        while True:
            start_seconds = time.time()
            self.cheat()
            self.now_count += 1
            if not self._can_continue_to_cheat():
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
