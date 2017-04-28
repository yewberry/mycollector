#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import wx
import my_res as res
from ui_mainframe import MyMainFrame
from my_glob import LOG
from my_conf import MyConf
from my_session import MySession
from my_watchdog import MyWatchdog
from my_signalcenter import MySignalCenter
import my_models as MyModels

class MyApp(wx.App):

    def OnInit(self):
        LOG.debug("OnInit")
        # init conf
        MyConf(os.path.join(os.getcwd(), "my.settings"))
        # init session
        MySession(os.path.join(os.getcwd(), "my.session"))
        # init database
        MyModels.create_all_tables()

        self.wathcdog = MyWatchdog("E:\\TTT")
        self.signalcenter = MySignalCenter(1)
        self.signalcenter.subscribe(self.wathcdog.queue)

        self.wathcdog.start()
        self.signalcenter.start()

        # setup MainFrame
        frame = MyMainFrame(None, res.S_MF_TITLE)
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

    def OnExit(self):
        self.wathcdog.start()



