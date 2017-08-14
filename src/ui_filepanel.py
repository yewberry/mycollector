# -*- coding: utf-8 -*-
import os
import wx
import wx.dataview as dv
import wx.propgrid as wxpg
from blinker import signal

import my_res as res
import my_event as evt
import my_models as model
from my_glob import LOG

EVT_FOLDER_UPDATED = signal(evt.FOLDER_UPDATED)
EVT_FILE_CREATED = signal(evt.FILE_CREATED)
EVT_FILE_DELETED = signal(evt.FILE_DELETED)
EVT_FILE_MODIFIED = signal(evt.FILE_MODIFIED)

class MyFilePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        # pgm: property grid manger
        self._pgm = None
        self._dvc = dv.DataViewCtrl(self, style=wx.BORDER_THEME | dv.DV_ROW_LINES | dv.DV_VERT_RULES | dv.DV_MULTIPLE)
        self.model = MyFileModel()
        self._dvc.AssociateModel(self.model)
        self._dvc.AppendTextColumn(res.S_FP_FILE_NAME, 0, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(res.S_FP_FILE_EXT, 1, width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        self._dvc.AppendTextColumn(res.S_FP_MODIFY_TIME, 2, width=100, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        self._dvc.AppendTextColumn(res.S_FP_FILE_SIZE, 3, width=80, mode=dv.DATAVIEW_CELL_ACTIVATABLE)
        for c in self._dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self._dvc, 1, wx.EXPAND)
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.onEditingDone, self._dvc)
        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.onValueChanged, self._dvc)
        self.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED, self.onSelectChanged, self._dvc)

    ###########################################################################
    # Getter and Setter
    ###########################################################################
    @property
    def dvc(self):
        return self._dvc

    def getCurRowData(self):
        sel = self._dvc.GetSelection()
        if sel is None:
            return None
        row = self.model.GetRow(sel)
        dat = self.model.data[row]
        return dat

    ###########################################################################
    # Callback for Detail panel
    ###########################################################################
    def initDetailPanel(self, pgm):
        pgm.Clear()
        page = pgm.AddPage(res.S_BD_FILE_INFO)
        page.Append(wxpg.LongStringProperty(res.S_BD_FILE_NAME, "file_name"))
        page.Append(wxpg.StringProperty(res.S_BD_EXT, "file_ext"))
        page.Append(wxpg.StringProperty(res.S_BD_SIZE, "file_size"))
        page.Append(wxpg.StringProperty(res.S_BD_MD5, "md5"))
        page.Append(wxpg.StringProperty(res.S_BD_MODIFY_TIME, "last_modify_time"))
        page.Append(wxpg.LongStringProperty(res.S_BD_PATH, "path"))
        self._pgm = pgm

    ###########################################################################
    # Events Process
    ###########################################################################
    def onSelectChanged(self, evt):
        f = self.getCurRowData()
        if (f is None) or (self._pgm is None):
            return

        fn = self._pgm.SetPropertyValueString
        fn("file_name", f.name)
        fn("file_ext", f.ext if f.ext is not None else "")
        fn("file_size", str(round(float(f.size) / 1024 / 1024, 2)))
        fn("md5", f.md5)
        fn("last_modify_time", f.last_modify_time.strftime("%Y-%m-%d %H:%M:%S"))
        fn("path", f.path)

    def OnDeleteRows(self, evt):
        items = self._dvc.GetSelections()
        rows = [self.model.GetRow(item) for item in items]
        self.model.DeleteRows(rows)

    def onEditingDone(self, evt):
        pass

    def onValueChanged(self, evt):
        pass

    def onReload(self, pth):
        pass

    @EVT_FOLDER_UPDATED.connect
    def onFolderUpdated(self, **kw):
        dat = model.File.getItems()
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
class MyFileModel(dv.PyDataViewIndexListModel):
    def __init__(self):
        dv.PyDataViewIndexListModel.__init__(self)
        self.data = model.File.getItems()
        self.Reset(len(self.data))

    def GetColumnType(self, col):
        return "string"

    def GetValueByRow(self, row, col):
        f = self.data[row]
        if col == 0:
            c = f.name
        elif col == 1:
            c = f.ext
        elif col == 2:
            c = f.last_modify_time.strftime("%Y-%m-%d %H:%M:%S")
        elif col == 3:
            c = round(float(f.size) / 1024 / 1024, 2)
        else:
            c = ""
        return c

    def SetValueByRow(self, value, row, col):
        pass

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
        f, _ = model.File.check(fp)
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


