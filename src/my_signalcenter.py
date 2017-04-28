# -*- coding: utf-8 -*-
import threading
import time
from blinker import signal

class MySignalCenter(threading.Thread):
    def __init__(self, interval):
        super(MySignalCenter, self).__init__()
        self.interval = interval
        self.thread_stop = False
        self.queues = []

    def run(self):
        while not self.thread_stop:
            for q in self.queues:
                if not q.empty():
                    r = q.get()
                    sig = signal(r["signal"])
                    sig.send(self, data=r["data"])
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True

    def subscribe(self, queue):
        self.queues.append(queue)




