# -*- coding: utf-8 -*-
import wx
from wx.lib.mixins import treemixin

class BookTreeMixin(treemixin.VirtualTree, treemixin.DragAndDrop, treemixin.ExpansionState):
    def __init__(self, *args, **kwargs):
        super(BookTreeMixin, self).__init__(*args, **kwargs)
        self.model = kwargs.pop('treemodel')
        self.CreateImageList()

    def CreateImageList(self):
        size = (16, 16)
        self.imageList = wx.ImageList(*size)
        for art in wx.ART_FOLDER, wx.ART_FILE_OPEN, wx.ART_NORMAL_FILE:
            self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER,
                                                        size))
        self.AssignImageList(self.imageList)

    def OnGetItemText(self, indices):
        return self.model.GetText(indices)

    def OnGetChildrenCount(self, indices):
        return self.model.GetChildrenCount(indices)

    def OnGetItemFont(self, indices):
        # Show how to change the item font. Here we use a small font for
        # items that have children and the default font otherwise.
        if self.model.GetChildrenCount(indices) > 0:
            return wx.SMALL_FONT
        else:
            return super(BookTreeMixin, self).OnGetItemFont(indices)

    def OnGetItemTextColour(self, indices):
        # Show how to change the item text colour. In this case second level
        # items are coloured red and third level items are blue. All other
        # items have the default text colour.
        if len(indices) % 2 == 0:
            return wx.RED
        elif len(indices) % 3 == 0:
            return wx.BLUE
        else:
            return super(BookTreeMixin, self).OnGetItemTextColour(indices)

    def OnGetItemBackgroundColour(self, indices):
        # Show how to change the item background colour. In this case the
        # background colour of each third item is green.
        if indices[-1] == 2:
            return wx.GREEN
        else:
            return super(BookTreeMixin, self).OnGetItemBackgroundColour(indices)

    def OnGetItemImage(self, indices, which):
        # Return the right icon depending on whether the item has children.
        if which in [wx.TreeItemIcon_Normal, wx.TreeItemIcon_Selected]:
            if self.model.GetChildrenCount(indices):
                return 0
            else:
                return 2
        else:
            return 1

    def OnDrop(self, dropTarget, dragItem):
        dropIndex = self.GetIndexOfItem(dropTarget)
        dropText = self.model.GetText(dropIndex)
        dragIndex = self.GetIndexOfItem(dragItem)
        dragText = self.model.GetText(dragIndex)
        self.model.MoveItem(dragIndex, dropIndex)
        self.GetParent().RefreshItems()

class MyBookTree(BookTreeMixin, wx.TreeCtrl):
    def __init__(self, parent):
        wx.TreeCtrl.__init__(self, parent, -1, size=wx.Size(160, 250), style=wx.TR_DEFAULT_STYLE | wx.NO_BORDER)
        root = self.AddRoot("AUI Project")
        items = []
        imglist = wx.ImageList(16, 16, True, 2)
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, wx.Size(16, 16)))
        imglist.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16)))
        self.AssignImageList(imglist)
        items.append(self.AppendItem(root, "Item 1", 0))
        items.append(self.AppendItem(root, "Item 2", 0))
        items.append(self.AppendItem(root, "Item 3", 0))
        items.append(self.AppendItem(root, "Item 4", 0))
        items.append(self.AppendItem(root, "Item 5", 0))
        for ii in xrange(len(items)):
            id = items[ii]
            self.AppendItem(id, "Subitem 1", 1)
            self.AppendItem(id, "Subitem 2", 1)
            self.AppendItem(id, "Subitem 3", 1)
            self.AppendItem(id, "Subitem 4", 1)
            self.AppendItem(id, "Subitem 5", 1)
        self.root = root
        self.Expand(root)

class BookTreeModel(object):
    ''' Each domain object is simply a two-tuple consisting of
    a label and a list of child tuples, i.e. (label, [list of child tuples]).
    '''
    def __init__(self, *args, **kwargs):
        self.items = []
        self.itemCounter = 0
        super(BookTreeModel, self).__init__(*args, **kwargs)

    def GetItem(self, indices):
        text, children = 'Hidden root', self.items
        for index in indices:
            text, children = children[index]
        return text, children

    def GetText(self, indices):
        return self.GetItem(indices)[0]

    def GetChildren(self, indices):
        return self.GetItem(indices)[1]

    def GetChildrenCount(self, indices):
        return len(self.GetChildren(indices))

    def SetChildrenCount(self, indices, count):
        children = self.GetChildren(indices)
        while len(children) > count:
            children.pop()
        while len(children) < count:
            children.append(('item %d'%self.itemCounter, []))
            self.itemCounter += 1

    def MoveItem(self, itemToMoveIndex, newParentIndex):
        itemToMove = self.GetItem(itemToMoveIndex)
        newParentChildren = self.GetChildren(newParentIndex)
        newParentChildren.append(itemToMove)
        oldParentChildren = self.GetChildren(itemToMoveIndex[:-1])
        oldParentChildren.remove(itemToMove)

