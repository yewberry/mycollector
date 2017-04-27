# -*- coding: utf-8 -*-
import multiprocessing
from watchdog.observers import Observer
from my_watchdog_handler import MyWatchdogHandler

class MyWatchdog(multiprocessing.Process):
    def __init__(self, path):
        multiprocessing.Process.__init__(self)
        self.path = path
        self.observer = None
        self._queue = multiprocessing.Queue(2)

    def run(self):
        event_handler = MyWatchdogHandler(self._queue)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        self.observer.join()

    @property
    def queue(self):
        return self._queue





