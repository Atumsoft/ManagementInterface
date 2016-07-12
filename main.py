from mainController import Controller
import wx


if __name__ == '__main__':
    app = wx.App()
    program = Controller()
    program.show()
    app.MainLoop()