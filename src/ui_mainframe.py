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
from ui_booktree import MyBookTree
from ui_filepanel import MyFilePanel
from ui_bookpanel import MyBookPanel
from ui_detailpanel import MyDetailPanel

from blinker import signal

###########################################################################
# MENU IDs
###########################################################################
ID_OPEN = wx.NewId()
ID_EXIT = wx.NewId()
ID_SETTINGS = wx.NewId()

class MyMainFrame(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title, style=wx.DEFAULT_FRAME_STYLE)
        self.cfg = MyConf()
        self.filepanel = None
        self.booktree = None
        self.bookpanel = None
        self.notebook = None
        self.detailpanel = None
        self.statusbar = None
        self._session = None

        self._mgr = wx.aui.AuiManager(self)
        self.worker_queue = multiprocessing.Queue(10)
        self.wathcdog = MyWatchdog(self.cfg.get("monitorFolders")[0])
        self.signalcenter = MySignalCenter()

        # Set system menu icon
        self.SetIcon(res.m_title.GetIcon())
        self.load_session()
        self.create_client_area()

        self.signalcenter.subscribe(self.wathcdog.queue)
        self.signalcenter.subscribe(self.worker_queue)
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
        self.booktree = MyBookTree(self)
        self.notebook = wx.aui.AuiNotebook(self, style=wx.aui.AUI_NB_TOP |
                            wx.aui.AUI_NB_TAB_SPLIT | wx.aui.AUI_NB_TAB_MOVE | wx.aui.AUI_NB_SCROLL_BUTTONS)
        self.filepanel = MyFilePanel(self.notebook)
        self.bookpanel = MyBookPanel(self.notebook)
        self.notebook.AddPage(self.filepanel, res.S_MF_ALL_TITLE)
        self.notebook.AddPage(self.bookpanel, res.S_MF_BOOK_TITLE)
        self.notebook.AddPage(wx.Panel(self.notebook), res.S_MF_MUSIC_TITLE)
        self.notebook.AddPage(wx.Panel(self.notebook), res.S_MF_VIDEO_TITLE)
        self.detailpanel = MyDetailPanel(self)

        self.filepanel.initDetailPanel(self.detailpanel.pgm)

        # self._mgr.AddPane(self.booktree, wx.aui.AuiPaneInfo().
        #                   Name("test8").Caption("Tree Pane").
        #                   Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.booktree, wx.LEFT, 'Pane Number One')
        self._mgr.AddPane(self.notebook, wx.CENTER)
        self._mgr.AddPane(self.detailpanel, wx.RIGHT, res.S_BD_TITLE)
        self._mgr.Update()
        self.signalcenter.add_sender_map(self.bookpanel,
                                         "EVT_FOLDER_UPDATED",
                                         "EVT_FILE_CREATED",
                                         "EVT_FILE_DELETED",
                                         "EVT_FILE_MODIFIED")

    def create_statusbar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-6, -1, -1])
        self.statusbar.SetStatusText("Ready.", 0)
        self.statusbar.SetStatusText("Line", 1)
        self.statusbar.SetStatusText("Type", 2)

    ###########################################################################
    # Session management
    ###########################################################################
    def load_session(self):
        # Set pos size
        s = MySession().get(MyMainFrame.__name__)
        if s is None:
            self.SetSize((1000, 600))
            self.Center()
        else:
            self.SetSize(s["size"])
            self.SetPosition(s["pos"])
        self._session = s

    def save_session(self):
        pos = self.GetPosition()
        size = self.GetSize()
        MySession().set(MyMainFrame.__name__, {"pos": pos, "size": size})
        LOG.debug({"pos": pos, "size": size})

    ###########################################################################
    # Subprocess init
    ###########################################################################
    def start_worker(self):
        self.signalcenter.start()
        self.wathcdog.start()
        p = multiprocessing.Process(target=MyWorker.sync_files_info,
                                    args=(self.cfg.get("monitorFolders")[0], self.worker_queue))
        p.start()

    ###########################################################################
    # Events Process
    ###########################################################################
    def bind_events(self):
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnOpenFile, id=ID_OPEN)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.onNotebookPageChanged, self.notebook)

    def OnCloseWindow(self, evt):
        self.wathcdog.stop()
        self.save_session()
        self.Destroy()

    def OnOpenFile(self, evt):
        self.wathcdog.stop()

    def onNotebookPageChanged(self, evt):
        panel = self.notebook.GetCurrentPage()
        panel.initDetailPanel(self.detailpanel.pgm)

