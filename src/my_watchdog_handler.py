# -*- coding: utf-8 -*-
from watchdog.events import RegexMatchingEventHandler
import my_event as evt

class MyWatchdogHandler(RegexMatchingEventHandler):
    def __init__(self, parent, regex_list=[r".*"]):
        super(MyWatchdogHandler, self).__init__(regex_list)
        self.parent = parent

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            self.parent.onFileChanged(evt.FILE_CREATED, event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            self.parent.onFileChanged(evt.FILE_DELETED, event.src_path)

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            self.parent.onFileChanged(evt.FILE_MODIFIED, event.src_path)

    def on_moved(self, event):
        print("move", event.src_path, event.dest_path)

