# -*- coding: utf-8 -*-
import wx
import my_res as res
from my_glob import LOG
from my_session import MySession

###########################################################################
# MENU IDs
###########################################################################
ID_OPEN = wx.NewId()
ID_EXIT = wx.NewId()
ID_SETTINGS = wx.NewId()

class MyMainFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        self._statusbar = None
        self._session = None

        # Set system menu icon
        self.SetIcon(res.m_title.GetIcon())
        self.load_session()
        self.create_client_area()

    ###########################################################################
    # UI Process
    ###########################################################################
    def create_client_area(self):
        self.create_menubar()
        # self.createToolbar()
        self.create_panels()
        self.create_statusbar()
        self.bind_events()

    def create_menubar(self):
        mb = wx.MenuBar()
        file_menu = wx.Menu()
        item = wx.MenuItem(file_menu, ID_OPEN, u"打开", u"打开文件")
        item.SetBitmap(res.m_open.GetBitmap())
        file_menu.AppendItem(item)
        file_menu.AppendSeparator()

        item = wx.MenuItem(file_menu, ID_EXIT, u"关闭\tCtrl+Q", u"关闭应用")
        item.SetBitmap(res.m_exit.GetBitmap())
        file_menu.AppendItem(item)

        options_menu = wx.Menu()
        item = wx.MenuItem(file_menu, ID_SETTINGS, u"设置", u"设置应用")
        item.SetBitmap(res.m_settings.GetBitmap())
        options_menu.AppendItem(item)

        mb.Append(file_menu, u"文件")
        mb.Append(options_menu, u"选项")
        self.SetMenuBar(mb)

    def create_panels(self):
        pass

    def create_statusbar(self):
        self._statusbar = self.CreateStatusBar()
        self._statusbar.SetFieldsCount(3)
        self._statusbar.SetStatusWidths([-6, -1, -1])
        self._statusbar.SetStatusText("Ready.", 0)
        self._statusbar.SetStatusText("Line", 1)
        self._statusbar.SetStatusText("Type", 2)

    ###########################################################################
    # Session Process
    ###########################################################################
    def load_session(self):
        # Set pos size
        s = MySession().get(MyMainFrame.__name__)
        if s is None:
            self.SetSize((800, 600))
            self.Center()
        else:
            self.SetSize(s["size"])
            self.SetPosition(s["pos"])
        self._session = s

    def save_session(self):
        pos = self.GetPosition()
        size = self.GetSize()
        MySession().set(MyMainFrame.__name__, {"pos": pos, "size": size})

    ###########################################################################
    # Events Process
    ###########################################################################
    def bind_events(self):
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_OPEN)

    def OnCloseWindow(self, evt):
        self.save_session()
        self.Destroy()

    def OnOpenFile(self, evt):
        pass




