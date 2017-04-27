# -*- coding: utf-8 -*-
from watchdog.events import RegexMatchingEventHandler

class MyWatchdogHandler(RegexMatchingEventHandler):


    def __init__(self, queue=None, regex_list=[r".*"]):
        super(MyWatchdogHandler, self).__init__(regex_list)
        self.queue = queue

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            self.queue.put({"signal": "ready", "data": "xixi"})
            print(event.event_type, event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            self.queue.put({"signal": "ready", "data": "xixi"})
            print(event.event_type, event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            print(event.event_type, event.src_path)

    def on_moved(self, event):
        print("move", event.src_path, event.dest_path)

