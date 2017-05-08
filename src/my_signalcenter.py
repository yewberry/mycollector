# -*- coding: utf-8 -*-
import threading
import time
from blinker import signal
from my_glob import LOG

class MySignalCenter(threading.Thread):
    def __init__(self, interval=1):
        super(MySignalCenter, self).__init__()
        self.interval = interval
        self.thread_stop = False
        self.queues = []
        self.sender_map = {}

    def run(self):
        while not self.thread_stop:
            for q in self.queues:
                if not q.empty():
                    r = q.get()
                    LOG.debug(r)
                    signal_str = r["signal"]
                    sender = self
                    if signal_str in self.sender_map.keys():
                        sender = self.sender_map[signal_str]
                    sig = signal(r["signal"])
                    sig.send(sender, data=r["data"])
            time.sleep(self.interval)

    def stop(self):
        self.thread_stop = True

    def subscribe(self, queue):
        self.queues.append(queue)

    def unsubscribe(self, queue):
        self.queues.remove(queue)

    def add_sender_map(self, sender, *msgs):
        for m in msgs:
            self.sender_map[m] = sender




