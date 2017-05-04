#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import wx
import my_res as res
from ui_mainframe import MyMainFrame
from my_glob import LOG
from my_conf import MyConf
from my_session import MySession
import my_models as models
import my_glob as G

class MyApp(wx.App):

    def OnInit(self):
        t = G.time_start()
        LOG.debug("OnInit")
        # init conf
        MyConf(os.path.join(os.getcwd(), "my.settings"))
        # init session
        MySession(os.path.join(os.getcwd(), "my.session"))
        # init database
        models.create_all_tables()
        # setup MainFrame
        frame = MyMainFrame(None, res.S_MF_TITLE)
        self.SetTopWindow(frame)
        frame.Show(True)
        LOG.debug(G.time_end(t))
        return True

    def OnExit(self):
        # exit but main process still there why?
        wx.Exit()




