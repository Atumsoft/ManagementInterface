# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Feb 16 2016)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class MainFrame
###########################################################################

class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(674, 425), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.statusBar1 = self.CreateStatusBar(3, wx.ST_SIZEGRIP, wx.ID_ANY)
        self.m_menubar1 = wx.MenuBar(0)
        self.menuFile = wx.Menu()
        self.menuExit = wx.MenuItem(self.menuFile, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.AppendItem(self.menuExit)

        self.m_menubar1.Append(self.menuFile, u"File")

        self.menuHelp = wx.Menu()
        self.menuShowLog = wx.MenuItem(self.menuHelp, wx.ID_ANY, u"Show Diagnostic Info...", wx.EmptyString,
                                       wx.ITEM_NORMAL)
        self.menuHelp.AppendItem(self.menuShowLog)

        self.m_menubar1.Append(self.menuHelp, u"Help")

        self.SetMenuBar(self.m_menubar1)

        self.timer1 = wx.Timer()
        self.timer1.SetOwner(self, wx.ID_ANY)
        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_splitter2 = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D)
        self.m_splitter2.Bind(wx.EVT_IDLE, self.m_splitter2OnIdle)
        self.m_splitter2.SetMinimumPaneSize(50)

        self.m_panel1 = wx.Panel(self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"Virtual Adapters", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer4.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.lstAdapters = wx.ListCtrl(self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer4.Add(self.lstAdapters, 1, wx.ALL | wx.EXPAND, 5)

        self.btnCreate = wx.Button(self.m_panel1, wx.ID_ANY, u"Create New...", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer4.Add(self.btnCreate, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_panel1.SetSizer(bSizer4)
        self.m_panel1.Layout()
        bSizer4.Fit(self.m_panel1)
        self.m_panel2 = wx.Panel(self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer5 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText2 = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Detected Devices", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer5.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.lstDevices = wx.ListCtrl(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer5.Add(self.lstDevices, 1, wx.ALL | wx.EXPAND, 5)

        self.btnRefresh = wx.Button(self.m_panel2, wx.ID_ANY, u"Refresh List", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer5.Add(self.btnRefresh, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_panel2.SetSizer(bSizer5)
        self.m_panel2.Layout()
        bSizer5.Fit(self.m_panel2)
        self.m_splitter2.SplitVertically(self.m_panel1, self.m_panel2, 334)
        bSizer3.Add(self.m_splitter2, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer3)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def m_splitter2OnIdle(self, event):
        self.m_splitter2.SetSashPosition(334)
        self.m_splitter2.Unbind(wx.EVT_IDLE)


