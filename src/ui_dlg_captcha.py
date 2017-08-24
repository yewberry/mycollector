# -*- coding: utf-8 -*-
import wx
class MyCaptchaDialog(wx.Dialog):
    def __init__(self, parent, title, pth):
        wx.Dialog.__init__(self, parent, -1, title,
                           size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE)
        png = wx.Image(pth, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        sizer = wx.BoxSizer(wx.VERTICAL)
        label = wx.StaticText(self, -1, u"输入图片文字")
        text = wx.TextCtrl(self, -1, "", size=(80, -1))
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(png, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)
        self.text = text

    def get_text(self):
        return self.text.Value()

