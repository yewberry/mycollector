# -*- coding: utf-8 -*-
import os
import wx
import wx.dataview as dv
import wx.propgrid as wxpg
from blinker import signal

import my_res as res
import my_event as evt
from my_glob import LOG
from my_models import File
from my_models import Ebook

EVT_FOLDER_UPDATED = signal(evt.FOLDER_UPDATED)
EVT_FILE_CREATED = signal(evt.FILE_CREATED)
EVT_FILE_DELETED = signal(evt.FILE_DELETED)
EVT_FILE_MODIFIED = signal(evt.FILE_MODIFIED)

class MyBookPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self._pgm = None
        self._dvc = dv.DataViewCtrl(self, style=wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE)
        self.model = MyBookModel()
        self._dvc.AssociateModel(self.model)
        self._dvc.AppendTextColumn(u"书名", 0, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(u"国别", 1, width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(u"作者", 2, width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(u"译者", 3, width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(u"出版时间", 4, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(u"出版社", 5, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(u"大小(MB)", 6, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        for c in self._dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._dvc, 1, wx.EXPAND)
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.OnEditingDone, self._dvc)
        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnValueChanged, self._dvc)
        self.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.onSelectChanged, self._dvc)

    ###########################################################################
    # Getter and Setter
    ###########################################################################
    @property
    def dvc(self):
        return self._dvc

    def getCurRowData(self):
        sel = self._dvc.GetSelections()[0]
        if sel is None:
            return None
        row = self.model.GetRow(sel)
        dat = self.model.data[row]
        return dat

    ###########################################################################
    # Callback Method
    ###########################################################################
    def initDetailPanel(self, pgm):
        pgm.Clear()
        page = pgm.AddPage("Page 1 - Testing All")
        page.Append(wxpg.PropertyCategory(res.S_BD_BOOK_INFO))
        page.Append(wxpg.LongStringProperty(res.S_BD_NAME, "book_name"))
        page.Append(wxpg.StringProperty(res.S_BD_AUTHOR, "author"))
        page.Append(wxpg.LongStringProperty(res.S_BD_DESC, "notes"))
        page.Append(wxpg.PropertyCategory(res.S_BD_FILE_INFO))
        page.Append(wxpg.StringProperty(res.S_BD_EXT, "ext"))
        page.Append(wxpg.StringProperty(res.S_BD_MD5, "md5"))
        pgm.AddPage("Page 2 - Testing All")
        self._pgm = pgm

    ###########################################################################
    # Events Process
    ###########################################################################
    def onSelectChanged(self, evt):
        f = self.getCurRowData()
        if f is None:
            return
        eb = f.ebook.get()
        fn = self._pgm.SetPropertyValueString
        fn("book_name", eb.book_name)
        fn("author", eb.author if eb.author is not None else "")
        fn("notes", eb.notes if eb.notes is not None else "")
        fn("ext", f.ext)
        fn("md5", f.md5)

    def OnDeleteRows(self, evt):
        items = self._dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]
        self.model.DeleteRows(rows)

    def OnAddRow(self, evt):
        # Add some bogus data to a new row in the model's data
        id = len(self.model.data) + 1
        value = [str(id),
                 'new artist %d' % id,
                 'new title %d' % id,
                 'genre %d' % id]
        self.model.AddRow(value)

    def OnEditingDone(self, evt):
        pass

    def OnValueChanged(self, evt):
        pass

    def onReload(self, pth):
        pass

    @EVT_FOLDER_UPDATED.connect
    def onFolderUpdated(self, **kw):
        dat = File.getItems()
        self.model.data = dat
        self.model.Reset(len(dat))
        LOG.debug(kw["data"])

    @EVT_FILE_CREATED.connect
    def onFileCreate(self, **kw):
        self.model.addRow(kw["data"])

    @EVT_FILE_DELETED.connect
    def onFileDelete(self, **kw):
        self.model.deleteRow(kw["data"])

###########################################################################
# DVC model
###########################################################################
class MyBookModel(dv.PyDataViewIndexListModel):
    def __init__(self):
        dv.PyDataViewIndexListModel.__init__(self)
        self.data = File.getItems()
        self.Reset(len(self.data))

    def GetColumnType(self, col):
        return "string"

    def GetValueByRow(self, row, col):
        f = self.data[row]
        e = f.ebook[0]
        if col == 0:
            c = e.book_name
        elif col == 2:
            c = e.author
        elif col == 6:
            c = round(float(f.size) / 1024 / 1024, 2)
        else:
            c = ""
        return c

    def SetValueByRow(self, value, row, col):
        f = self.data[row]
        ebk_id = f.ebook[0].uid
        ebk = Ebook.get(Ebook.uid == ebk_id)
        if col == 0:
            ebk.book_name = value
        elif col == 2:
            ebk.author = value
        ebk.save()
        f.save()

    def GetColumnCount(self):
        return len(self.data[0])

    def GetCount(self):
        return len(self.data)

    def GetAttrByRow(self, row, col, attr):
        f = self.data[row]
        if f.invalid:
            attr.SetColour("gray")
            attr.SetItalic(True)
            return True
        elif col == 6:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    def Compare(self, item1, item2, col, ascending):
        if not ascending:  # swap sort order?
            item2, item1 = item1, item2
        row1 = self.GetRow(item1)
        row2 = self.GetRow(item2)
        fld = self.map[col]
        c1, c2 = "", ""
        if fld is not None:
            c1 = getattr(self.data[row1], fld)
            c2 = getattr(self.data[row2], fld)
        return cmp(c1, c2)

    def addRow(self, fp):
        pth = os.path.abspath(fp)
        idx = next((i for i, x in enumerate(self.data) if x.path == pth), [-1])
        f, _ = File.check(fp)
        if idx == -1:
            self.data.append(f)
            self.RowAppended()
        else:
            self.data[idx] = f
            self.RowChanged(idx)

    def deleteRow(self, fp):
        pth = os.path.abspath(fp)
        idx = next((i for i, x in enumerate(self.data) if x.path == pth))
        self.data[idx].remove()
        self.RowChanged(idx)
        # del self.data[idx]
        # self.RowDeleted(idx)

    def DeleteRows(self, rows):
        # make a copy since we'll be sorting(mutating) the list
        rows = list(rows)
        # use reverse order so the indexes don't change as we remove items
        rows.sort(reverse=True)

        for row in rows:
            # remove it from our data structure
            del self.data[row]
            # notify the view(s) using this model that it has been removed
            self.RowDeleted(row)


