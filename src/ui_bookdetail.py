# -*- coding: utf-8 -*-
import os
import wx
import wx.lib.evtmgr as em
import wx.dataview as dv
import wx.propgrid as wxpg
from blinker import signal

import my_res as res
from my_glob import LOG
from my_models import File
from my_models import Ebook

class MyBookDetail(wx.Panel):
    def __init__(self, parent, bookpanel):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, size=wx.Size(200, 150))
        self.bp = bookpanel
        self.pg = wxpg.PropertyGridManager(self,
                    style=wxpg.PG_SPLITTER_AUTO_CENTER | wxpg.PG_BOLD_MODIFIED |
                          wxpg.PG_NO_INTERNAL_BORDER | wxpg.PG_TOOLBAR)
        self.pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)
        self.pg.GetGrid().SetSplitterLeft()
        page = self.pg.AddPage("Page 1 - Testing All")
        page.Append(wxpg.PropertyCategory(res.S_BD_BOOK_INFO))
        page.Append(wxpg.LongStringProperty(res.S_BD_NAME, "book_name"))
        page.Append(wxpg.StringProperty(res.S_BD_AUTHOR, "author"))
        page.Append(wxpg.LongStringProperty(res.S_BD_DESC, "notes"))
        page.Append(wxpg.PropertyCategory(res.S_BD_FILE_INFO))
        page.Append(wxpg.StringProperty(res.S_BD_EXT, "ext"))
        page.Append(wxpg.StringProperty(res.S_BD_MD5, "md5"))
        self.pg.AddPage("Page 2 - Testing All")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.pg, 1, wx.EXPAND)
        self.SetSizer(sizer)
        em.eventManager.Register(self.onBookListChanged, dv.EVT_DATAVIEW_SELECTION_CHANGED, self.bp.dvc)

    def onBookListChanged(self, evt):
        f = self.bp.getCurRowData()
        if f is None:
            return
        self.updateProperty(f)

    def updateProperty(self, f):
        eb = f.ebook.get()
        fn = self.pg.SetPropertyValueString
        fn("book_name", eb.book_name)
        fn("author", eb.author if eb.author is not None else "")
        fn("notes", eb.notes if eb.notes is not None else "")
        fn("ext", f.ext)
        fn("md5", f.md5)



