# -*- coding: utf-8 -*-
from watchdog.events import RegexMatchingEventHandler

class MyWatchdogHandler(RegexMatchingEventHandler):
    def __init__(self, parent, queue=None, regex_list=[r".*"]):
        super(MyWatchdogHandler, self).__init__(regex_list)
        self.parent = parent
        self.queue = queue

    def notify(self, dat):
        self.queue.put(dat)

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            self.parent.onFileCreated(event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            self.notify({"signal": "EVT_FILE_DELETED", "data": u"{}".format(event.src_path)})

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            self.notify({"signal": "EVT_FILE_MODIFIED", "data": u"{}".format(event.src_path)})

    def on_moved(self, event):
        print("move", event.src_path, event.dest_path)

