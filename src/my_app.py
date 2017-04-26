#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import wx
from ui_mainframe import MyMainFrame
from my_glob import LOG
from my_conf import MyConf
from my_session import MySession

class MyApp(wx.App):
    """
    This is app class for MyCoder
    """
    def OnInit(self):
        LOG.debug("OnInit")
        # init conf
        MyConf(os.path.join(os.getcwd(), "my.settings"))
        # init session
        MySession(os.path.join(os.getcwd(), "my.session"))
        # setup MainFrame
        frame = MyMainFrame(None, "MyCoder")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

    def OnExit(self):
        pass


