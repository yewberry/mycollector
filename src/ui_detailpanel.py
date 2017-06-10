# -*- coding: utf-8 -*-
import os
import wx
import wx.lib.evtmgr as em
import wx.propgrid as wxpg
from blinker import signal
from my_glob import LOG

class MyDetailPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, size=wx.Size(200, 150))
        self._pgm = wxpg.PropertyGridManager(self,
                    style=wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_BOLD_MODIFIED | wxpg.PG_HIDE_CATEGORIES |
                          wxpg.PG_NO_INTERNAL_BORDER | wxpg.PG_TOOLBAR | wxpg.PG_HIDE_MARGIN)
        self._pgm.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)
        self._pgm.GetGrid().SetSplitterLeft()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._pgm, 1, wx.EXPAND)
        self.SetSizer(sizer)

    @property
    def pgm(self):
        return self._pgm




