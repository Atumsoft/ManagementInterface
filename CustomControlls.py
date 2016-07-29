import socket

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
        self.window.Bind(wx.EVT_LEFT_UP, self.checkPos, self.window.txtOutput)

        self.last_line_visibility = ''

    def ShowModal(self, *args, **kwargs):
        self.window.Show()
        self.update()

    def update(self, event=None):
        curVal = self.window.txtOutput.GetValue()
        curPos = self.window.txtOutput.GetScrollPos(wx.VERTICAL)
        if curVal == self.stdout.getvalue(): return
        self.window.txtOutput.SetValue(self.stdout.getvalue())
        self.window.txtOutput.ScrollLines(curPos)

        if self.last_line_visibility == 'VISIBLE':
            self.window.txtOutput.ScrollLines(-1)

    def checkPos(self, event=None):
        """
            scroll to bottom only if user is at the bottom
        """
        last_line_nr = self.window.txtOutput.PositionToXY(self.window.txtOutput.LastPosition)[1]
        first_visible_line = self.window.txtOutput.HitTest((0, 5))[2]  # 5 pixels from the margin - arbitrary
        last_visible_line = self.window.txtOutput.HitTest((0, self.window.txtOutput.GetSizeTuple()[1] - 5))[2]  # 5 px - ditto

        self.last_line_visibility = "VISIBLE" if first_visible_line <= last_line_nr <= last_visible_line else "INVISIBLE"  # first part not needed for the last line

        event.Skip()


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
        ipvalid = True
        try:
            socket.inet_aton(ip)
        except socket.error:
            ipvalid = False

        if not name:
            dlg = wx.MessageDialog(self.window, "please enter a valid name", "name error", style=wx.ICON_WARNING)
            dlg.ShowModal()

        elif self.adapterNameDict.get(name):
            dlg = wx.MessageDialog(self.window, "name already in use, must be unique", "name error", style=wx.ICON_WARNING)
            dlg.ShowModal()

        elif not len(ipFields) == 4 or not ipvalid:
            dlg = wx.MessageDialog(self.window, "please enter a valid IP address", "name error", style=wx.ICON_WARNING)
            dlg.ShowModal()

        else:
            event.Skip()