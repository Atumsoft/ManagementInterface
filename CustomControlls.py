from CustomViews import *
from cStringIO import StringIO
import sys
import wx
import threading


class DiagController:
    def __init__(self, stdout, *args, **kwargs):
        self.window = DiagDialog(*args, **kwargs)
        self.window.timer1.Start(1000)
        self.stdout = stdout
        self.window.Bind(wx.EVT_TIMER, self.update, self.window.timer1)

    def ShowModal(self, *args, **kwargs):
        self.window.Show()
        self.update()

    def update(self, event=None):
        curVal = self.window.txtOutput.GetValue()
        if curVal == self.stdout.getvalue: return
        self.window.txtOutput.SetValue(self.stdout.getvalue())


class AddController:
    def __init__(self, adapterNameDict={}, *args, **kwargs):
        self.window = dlgAddDevice(*args, **kwargs)
        self.window.Bind(wx.EVT_BUTTON, self.validate, self.window.btnOK)

        self.adapterNameDict = adapterNameDict

    def ShowModal(self, *args, **kwargs):
        return self.window.ShowModal()

    def validate(self, event):
        name = self.window.txtName.GetValue()
        ip = self.window.txtIP.GetValue()
        ipFields = ip.split('.')

        if not name:
            dlg = wx.MessageDialog(self.window, "please enter a valid name", "name error", style=wx.ICON_WARNING)
            dlg.ShowModal()

        elif self.adapterNameDict.get(name):
            dlg = wx.MessageDialog(self.window, "name already in use, must be unique", "name error", style=wx.ICON_WARNING)
            dlg.ShowModal()

        elif not len(ipFields) == 4:
            dlg = wx.MessageDialog(self.window, "please enter a valid IP address", "name error", style=wx.ICON_WARNING)
            dlg.ShowModal()

        else:
            event.Skip()