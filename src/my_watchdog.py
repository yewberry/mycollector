# -*- coding: utf-8 -*-
import multiprocessing
from watchdog.observers import Observer
from my_watchdog_handler import MyWatchdogHandler
import my_models as MyModels

class MyWatchdog(multiprocessing.Process):
    def __init__(self, path):
        multiprocessing.Process.__init__(self)
        self.daemon = True
        self.path = path
        self.observer = None
        self._queue = multiprocessing.Queue(2)

    def run(self):
        event_handler = MyWatchdogHandler(self, self._queue)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        self.observer.join()

    def onFileCreated(self, path):
        self.notify({"signal": "EVT_FILE_CREATED", "data": u"{}".format(path)})

    def notify(self, dat):
        self.queue.put(dat)

    def stop(self):
        self.observer.stop()

    @property
    def queue(self):
        return self._queue





