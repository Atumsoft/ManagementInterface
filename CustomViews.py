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
## Class DiagDialog
###########################################################################

class DiagDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                           size=wx.Size(620, 371), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.txtOutput = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                     wx.HSCROLL | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP)
        bSizer1.Add(self.txtOutput, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.timer1 = wx.Timer()
        self.timer1.SetOwner(self, wx.ID_ANY)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


###########################################################################
## Class dlgAddDevice
###########################################################################

class dlgAddDevice(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Add a Virtual Adapter", pos=wx.DefaultPosition,
                           size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        gSizer1 = wx.GridSizer(0, 2, 0, 0)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Name of Device:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText3.Wrap(-1)
        gSizer1.Add(self.m_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 5)

        self.txtName = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.txtName, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"IP Address to Assign:", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        gSizer1.Add(self.m_staticText4, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.txtIP = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.txtIP, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 5)

        gSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        gSizer1.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.btnOK = wx.Button(self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btnOK, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btnCancel = wx.Button(self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btnCancel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.SetSizer(gSizer1)
        self.Layout()
        gSizer1.Fit(self)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass


###########################################################################
## Class ConnectDialog
###########################################################################

class ConnectDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=wx.ID_ANY, title=u"Select a decive to connect to", pos=wx.DefaultPosition,
                           size=wx.Size(601, 292), style=wx.DEFAULT_DIALOG_STYLE)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.lstAdapters = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT)
        bSizer7.Add(self.lstAdapters, 1, wx.ALL | wx.EXPAND, 5)

        gSizer1 = wx.GridSizer(0, 3, 0, 0)

        self.btnGenerate = wx.Button(self, wx.ID_OPEN, u"Create Adapter", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btnGenerate, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.btnOK = wx.Button(self, wx.ID_OK, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btnOK, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.btnCancel = wx.Button(self, wx.ID_CANCEL, u"Cancel", wx.DefaultPosition, wx.DefaultSize, 0)
        gSizer1.Add(self.btnCancel, 0, wx.ALL, 5)

        bSizer7.Add(gSizer1, 0, wx.EXPAND, 5)

        self.SetSizer(bSizer7)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

