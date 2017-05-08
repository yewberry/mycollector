# -*- coding: utf-8 -*-
import wx
import wx.dataview as dv
from blinker import signal

from my_glob import LOG
from my_models import File
from my_models import Ebook

EVT_FOLDER_UPDATED = signal("EVT_FOLDER_UPDATED")
EVT_FILE_CREATED = signal("EVT_FILE_CREATED")
EVT_FILE_DELETED = signal("EVT_FILE_DELETED")
EVT_FILE_MODIFIED = signal("EVT_FILE_MODIFIED")

class MyBookPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.dvc = dv.DataViewCtrl(self,
                                   style=wx.BORDER_THEME
                                         | dv.DV_ROW_LINES
                                         # | dv.DV_HORIZ_RULES
                                         | dv.DV_VERT_RULES
                                         | dv.DV_MULTIPLE
                                   )
        self.model = MyBookModel()

        # Models can be shared between multiple DataViewCtrls, so this does not
        # assign ownership like many things in wx do.  There is some
        # internal reference counting happening so you don't really
        # need to hold a reference to it either, but we do for this
        # example so we can fiddle with the model from the widget
        # inspector or whatever.
        self.dvc.AssociateModel(self.model)

        self.dvc.AppendTextColumn(u"书名", 0, width=170, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn(u"国别", 1, width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn(u"作者", 2, width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn(u"译者", 3, width=50, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn(u"出版时间", 4, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn(u"出版社", 5, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)
        self.dvc.AppendTextColumn(u"大小(MB)", 6, width=80, mode=dv.DATAVIEW_CELL_EDITABLE)

        for c in self.dvc.Columns:
            c.Sortable = True
            c.Reorderable = True

        # set the Sizer property (same as SetSizer)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.Sizer.Add(self.dvc, 1, wx.EXPAND)

        # Bind some events so we can see what the DVC sends us
        self.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE, self.OnEditingDone, self.dvc)
        self.Bind(dv.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnValueChanged, self.dvc)

    def OnDeleteRows(self, evt):
        # Remove the selected row(s) from the model. The model will take care
        # of notifying the view (and any other observers) that the change has
        # happened.
        items = self.dvc.GetSelections()
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

    # Called to check if non-standard attributes should be used in the
    # cell at (row, col)
    def GetAttrByRow(self, row, col, attr):
        if col == 6:
            attr.SetColour('blue')
            attr.SetBold(True)
            return True
        return False

    # This is called to assist with sorting the data in the view.  The
    # first two args are instances of the DataViewItem class, so we
    # need to convert them to row numbers with the GetRow method.
    # Then it's just a matter of fetching the right values from our
    # data set and comparing them.  The return value is -1, 0, or 1,
    # just like Python's cmp() function.
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

