from systray import TaskBarIcon
import wx


if __name__ == '__main__':
    app = wx.App()
    program = TaskBarIcon()
    app.MainLoop()