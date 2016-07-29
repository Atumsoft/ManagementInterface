import wx
import images

from mainController import Controller

TRAY_TOOLTIP = 'Atumsoft Bridge Software'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item


class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        self.mainWindow = Controller()
        self.mainWindow.show()
        self.icon = wx.BitmapFromImage(images.getLogoImage())
        self.set_icon(self.icon)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Show Window', self.onShow)
        menu.AppendSeparator()
        create_menu_item(menu, 'Exit', self.onExit)
        return menu

    def set_icon(self, path):
        icon = wx.IconFromBitmap(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def on_left_down(self, event):
        pass
        event.Skip()

    def onShow(self, event):
        self.mainWindow.show()
    def onExit(self, event):
        self.mainWindow.destroy()
        wx.CallAfter(self.Destroy)

def main():
    app = wx.PySimpleApp()
    TaskBarIcon()
    app.MainLoop()


if __name__ == '__main__':
    main()