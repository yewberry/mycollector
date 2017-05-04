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
        self._queue = multiprocessing.Queue(2)
        self.evt = multiprocessing.Event()

    def run(self):
        event_handler = MyWatchdogHandler(self)
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()
        self.evt.wait()
        observer.stop()
        observer.join()

    def onFileChanged(self, sig, path):
        self.notify({"signal": sig, "data": u"{}".format(path)})

    def notify(self, dat):
        self.queue.put(dat)

    def stop(self):
        self.evt.set()

    @property
    def queue(self):
        return self._queue





