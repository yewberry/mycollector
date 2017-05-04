# -*- coding: utf-8 -*-
import wx
import wx.aui
import multiprocessing
import my_res as res
from my_glob import LOG
from my_conf import MyConf
from my_session import MySession
from my_watchdog import MyWatchdog
from my_signalcenter import MySignalCenter
import my_worker as MyWorker
from ui_bookpanel import MyBookPanel

from blinker import signal

###########################################################################
# MENU IDs
###########################################################################
ID_OPEN = wx.NewId()
ID_EXIT = wx.NewId()
ID_SETTINGS = wx.NewId()

EVT_FILE_CREATED = signal("EVT_FILE_CREATED")
EVT_FILE_DELETED = signal("EVT_FILE_DELETED")
EVT_FILE_MODIFIED = signal("EVT_FILE_MODIFIED")

class MyMainFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, style=wx.DEFAULT_FRAME_STYLE)
        self._statusbar = None
        self._session = None
        self.cfg = MyConf()

        self._mgr = wx.aui.AuiManager(self)

        self.wathcdog = MyWatchdog(self.cfg.get("monitorFolders")[0])
        self.signalcenter = MySignalCenter()
        self.signalcenter.subscribe(self.wathcdog.queue)

        # Set system menu icon
        self.SetIcon(res.m_title.GetIcon())
        self.load_session()
        self.create_client_area()
        self.start_worker()

    ###########################################################################
    # UI creation
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
        text1 = wx.TextCtrl(self, -1, 'Pane 1 - sample text',
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)

        text2 = wx.TextCtrl(self, -1, 'Pane 2 - sample text',
                            wx.DefaultPosition, wx.Size(200,150),
                            wx.NO_BORDER | wx.TE_MULTILINE)

        self.bookpanel = MyBookPanel(self)
        self._mgr.AddPane(text1, wx.LEFT, 'Pane Number One')
        self._mgr.AddPane(text2, wx.BOTTOM, 'Pane Number Two')
        self._mgr.AddPane(self.bookpanel, wx.CENTER)
        self._mgr.Update()

    def create_statusbar(self):
        self._statusbar = self.CreateStatusBar()
        self._statusbar.SetFieldsCount(3)
        self._statusbar.SetStatusWidths([-6, -1, -1])
        self._statusbar.SetStatusText("Ready.", 0)
        self._statusbar.SetStatusText("Line", 1)
        self._statusbar.SetStatusText("Type", 2)

    ###########################################################################
    # Session management
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
    # Subprocess init
    ###########################################################################
    def start_worker(self):
        self.signalcenter.start()
        self.wathcdog.start()
        p = multiprocessing.Process(target=MyWorker.sync_files_info,
                                    args=(self.cfg.get("monitorFolders")[0],))
        p.start()

    ###########################################################################
    # Events Process
    ###########################################################################
    def bind_events(self):
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_OPEN)

    def OnCloseWindow(self, evt):
        self.wathcdog.stop()
        self.save_session()
        self.Destroy()

    def OnOpenFile(self, evt):
        self.wathcdog.stop()

    @EVT_FILE_CREATED.connect
    def onFileCreated(self, **kw):
        print "onFileCreated", kw["data"]

    @EVT_FILE_DELETED.connect
    def onFileDeleted(self, **kw):
        print "onFileDeleted", kw["data"]

    @EVT_FILE_MODIFIED.connect
    def onFileModified(self, **kw):
        print "onFileModifiedkw", kw["data"]


