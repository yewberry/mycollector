# -*- coding: utf-8 -*-
import wx
import wx.aui
import multiprocessing

import my_res as res
import my_event as evt
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
from ui_netdiskpanel import MyNetDiskPanel

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
        self.netdiskpanel = None
        self._session = None
        self.monitorFolders = self.cfg.get("monitorFolders")

        self._mgr = wx.aui.AuiManager(self)
        self.worker_queue = multiprocessing.Queue(10)
        self.wathcdog = MyWatchdog(self.monitorFolders[0])
        self.signalcenter = MySignalCenter()

        # Set system menu icon
        self.SetIcon(res.m_title.GetIcon())
        self.loadSession()
        self.createClientArea()

        self.signalcenter.subscribe(self.wathcdog.queue)
        self.signalcenter.subscribe(self.worker_queue)
        self.startWorker()

    ###########################################################################
    # UI creation
    ###########################################################################
    def createClientArea(self):
        self.createMenubar()
        # self.createToolbar()
        self.createPanels()
        self.createStatusbar()
        self.bindEvents()

    def createMenubar(self):
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

        mb.Append(file_menu, res.S_MENU_FILE)
        mb.Append(options_menu, res.S_MENU_OPTION)
        self.SetMenuBar(mb)

    def createPanels(self):
        self.booktree = MyBookTree(self)
        self.notebook = wx.aui.AuiNotebook(self, style=wx.aui.AUI_NB_TOP |
                            wx.aui.AUI_NB_TAB_SPLIT | wx.aui.AUI_NB_TAB_MOVE | wx.aui.AUI_NB_SCROLL_BUTTONS)
        self.filepanel = MyFilePanel(self.notebook)
        self.bookpanel = MyBookPanel(self.notebook)
        self.netdiskpanel = MyNetDiskPanel(self.notebook)
        self.notebook.AddPage(self.netdiskpanel, res.S_MF_NETDISK_TITLE)
        self.notebook.AddPage(self.filepanel, res.S_MF_ALL_TITLE)
        self.notebook.AddPage(self.bookpanel, res.S_MF_BOOK_TITLE)
        self.notebook.AddPage(wx.Panel(self.notebook), res.S_MF_MUSIC_TITLE)
        self.notebook.AddPage(wx.Panel(self.notebook), res.S_MF_VIDEO_TITLE)
        self.detailpanel = MyDetailPanel(self)

        def_page = self.netdiskpanel
        self.notebook.SetSelection(self.notebook.GetPageIndex(def_page))
        def_page.initDetailPanel(self.detailpanel.pgm)

        # self._mgr.AddPane(self.booktree, wx.aui.AuiPaneInfo().
        #                   Name("test8").Caption("Tree Pane").
        #                   Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))

        self._mgr.AddPane(self.booktree, wx.LEFT, 'Pane Number One')
        self._mgr.AddPane(self.notebook, wx.CENTER)
        self._mgr.AddPane(self.detailpanel, wx.RIGHT, res.S_BD_TITLE)
        self._mgr.Update()
        self.signalcenter.addSenderMap(self.bookpanel,
                                       evt.FOLDER_UPDATED, evt.FILE_CREATED, evt.FILE_DELETED, evt.FILE_MODIFIED)

    def createStatusbar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-6, -1, -1])
        self.statusbar.SetStatusText("Ready.", 0)
        self.statusbar.SetStatusText("Line", 1)
        self.statusbar.SetStatusText("Type", 2)

    ###########################################################################
    # Session management
    ###########################################################################
    def loadSession(self):
        # Set pos size
        s = MySession().get(MyMainFrame.__name__)
        if s is None:
            self.SetSize((1000, 600))
            self.Center()
        else:
            self.SetSize(s["size"])
            self.SetPosition(s["pos"])
        self._session = s

    def saveSession(self):
        pos = self.GetPosition()
        size = self.GetSize()
        MySession().set(MyMainFrame.__name__, {"pos": pos, "size": size})
        LOG.debug({"pos": pos, "size": size})

    ###########################################################################
    # Subprocess init
    ###########################################################################
    def startWorker(self):
        self.signalcenter.start()
        self.wathcdog.start()
        p = multiprocessing.Process(target=MyWorker.sync_files_info,
                                    args=(self.monitorFolders[0], self.worker_queue))
        p.start()

    ###########################################################################
    # Events Process
    ###########################################################################
    def bindEvents(self):
        self.Bind(wx.EVT_CLOSE, self.onCloseWindow)
        self.Bind(wx.EVT_MENU, self.onCloseWindow, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.onOpenFile, id=ID_OPEN)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.onNotebookPageChanged, self.notebook)

    def onCloseWindow(self, evt):
        self.wathcdog.stop()
        self.saveSession()
        self.Destroy()

    def onOpenFile(self, evt):
        import PyV8
        import requests
        import re
        import json

        # login_tangram_xxxxxxx.js
        ctxt = PyV8.JSContext()
        ctxt.enter()
        gid = ctxt.eval("""
            (function(){
                return "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,
                    function(e) {
                        var t = 16 * Math.random() | 0,
                        n = "x" == e ? t: 3 & t | 8;
                        return n.toString(16)
                    }).toUpperCase()
            })
        """)
        tt = ctxt.eval("""
            (function(){
                return ""+(new Date).getTime();
            })
        """)
        callback = ctxt.eval("""
            (function(){
                return "bd__cbs__" + Math.floor(Math.random() * 2147483648).toString(36);
            })
        """)

        gid = gid()
        usr = "13813000397"
        cookies = {}

        r = requests.get("http://pan.baidu.com")
        baidu_id = r.cookies["BAIDUID"]
        print "BAIDUID:", baidu_id
        cookies["BAIDUID"] = baidu_id

        r = requests.get("https://passport.baidu.com/v2/api/?getapi", params={
            "tpl": "netdisk",
            "subpro": "netdisk_web",
            "apiver": "v3",
            "tt": tt(),
            "class": "login",
            "logintype": "basicLogin",
            "gid": gid,
            "callback": callback()
        }, cookies=cookies)
        json_str = re.findall(r"\((.+?)\)", r.text)[0]
        json_str = json_str.replace("\'", "\"")
        o = json.loads(json_str)
        token = o["data"]["token"]
        print "token:", token, o
        cookies["HOSUPPORT"] = "1"

        r = requests.get("https://passport.baidu.com/v2/api/?logincheck", params={
            "token": token,
            "tpl": "netdisk",
            "subpro": "netdisk_web",
            "apiver": "v3",
            "tt": tt(),
            "sub_source": "leadsetpwd",
            "username": usr,
            "isphone": "false",
            "dv": "",
            "callback": callback()
        }, cookies=cookies)
        ubi = r.cookies["UBI"]
        print "UBI:", ubi
        cookies["UBI"] = ubi

        payload = {
            "staticpage": "http://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html",
            "charset": "utf-8",
            "tpl": "netdisk",
            "subpro": "netdisk_web",
            "apiver": "v3",
            "codestring": "",
            "safeflg": "0",
            "u": "http://pan.baidu.com/disk/home",
            "isPhone": "false",
            "detect": "1",
            "quick_user": "0",
            "logintype": "basicLogin",
            "logLoginType": "pc_loginBasic",
            "idc": "",
            "loginmerge": "true",
            "foreignusername": "",
            "mem_pass": "on",
            "ppui_logintime": "7238",
            "countrycode": "",
            "fp_uid": "",
            "fp_info": "",
            "dv": "",

            "username": usr,
            "password": "yewyew",
            "token": token,
            "tt": tt(),
            "gid": gid,
            "callback": callback()
        }
        # r = requests.post("http://httpbin.org/post", data=payload)
        r = requests.post("https://passport.baidu.com/v2/api/?login", data=payload
                          , cookies=cookies)
        print r.text

    def onNotebookPageChanged(self, evt):
        panel = self.notebook.GetCurrentPage()
        panel.initDetailPanel(self.detailpanel.pgm)

