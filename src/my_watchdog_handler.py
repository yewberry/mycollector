# -*- coding: utf-8 -*-
from watchdog.events import RegexMatchingEventHandler
import my_file_tools as filetools
from my_models import File

class MyWatchdogHandler(RegexMatchingEventHandler):
    def __init__(self, parent, regex_list=[r".*"]):
        super(MyWatchdogHandler, self).__init__(regex_list)
        self.parent = parent

    def on_created(self, event):
        if event.is_directory:
            pass
        else:
            pth = event.src_path
            md5 = filetools.get_md5(pth)
            self.parent.onFileChanged({
                "path": pth,
                "md5": md5
            })

    def on_deleted(self, event):
        if event.is_directory:
            pass
        else:
            pth = event.src_path
            self.parent.onFileChanged({
                "path": pth,
                "md5": ""
            })

    def on_modified(self, event):
        if event.is_directory:
            pass
        else:
            pth = event.src_path
            md5 = filetools.get_md5(pth)
            f = File.get_by_path(pth)
            if (f is not None) and (f.md5 != md5):
                self.parent.onFileChanged({
                    "path": pth,
                    "md5": md5
                })

    def on_moved(self, event):
        if event.is_directory:
            pass
        else:
            print("move", event.src_path, event.dest_path)

