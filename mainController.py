import ctypes
import os

from mainView import MainFrame
from CustomControlls import DiagController, AddController

from cStringIO import StringIO
import sys
import wx
import API
import threading

sys.stdout = mystdout = StringIO()


class Controller:
    def __init__(self):
        # initialize view params
        self.mainWindow = MainFrame(None)
        self.mainWindow.timer1.Start(1000)
        self.mainWindow.statusBar1.SetStatusText('No connected Device', 0)

        self.mainWindow.lstAdapters.InsertColumn(0, 'Number', width=wx.COL_WIDTH_AUTOSIZE)
        self.mainWindow.lstAdapters.InsertColumn(1, 'Name', width=100)
        self.mainWindow.lstAdapters.InsertColumn(2, 'IP Address', width=100)
        self.mainWindow.lstAdapters.InsertColumn(3, 'Capturing', width=wx.COL_WIDTH_AUTOSIZE)

        self.mainWindow.lstDevices.InsertColumn(0, 'Name', width=100)
        self.mainWindow.lstDevices.InsertColumn(1, 'IP Address', width=100)
        self.mainWindow.lstDevices.InsertColumn(1, 'Mac Address', width=100)

        # setup bindings
        self.mainWindow.Bind(wx.EVT_MENU, self.showDiag, self.mainWindow.menuShowLog)
        self.mainWindow.Bind(wx.EVT_TIMER, self.update, self.mainWindow.timer1)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.createNewAdapter, self.mainWindow.btnCreate)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.scan, self.mainWindow.btnRefresh)

        # class vars
        self.scanning = False
        self.tunTapDict = {}

        # networking vars
        self.networkGatewayIP, self.networkIface = API.AtumsoftUtils.findGateWay()
        self.networkIfaceIP = API.AtumsoftUtils.getIP(self.networkIface)

        # dictionaries to make sure names are unique
        self.adapterNameDict = {}

        # needs to be run as admin if not already
        checkForAdmin()

    def show(self):
        self.mainWindow.Show()

    def showDiag(self, event):
        dlg = DiagController(mystdout,self.mainWindow)
        dlg.ShowModal()

    def exit(self):
        exit(0)

    def startCapture(self, event):
        pass

    def update(self, event):
        if not self.scanning: return

        if len(self.mainWindow.statusBar1.GetStatusText(2)) >= len('scanning...'):
            self.mainWindow.statusBar1.SetStatusText('scanning', 2)
        else:
            self.mainWindow.statusBar1.SetStatusText(self.mainWindow.statusBar1.GetStatusText(2) + '.', 2)

    def scan(self, event):
        if not self.scanning:
            self.scanning = True
            self.mainWindow.statusBar1.SetStatusText('scanning', 2)
            self.scanThread = threading.Thread(target=self._scan)
            self.scanThread.setDaemon(True)
            self.scanThread.start()
            self.mainWindow.btnRefresh.SetLabel('Stop Scan')
        else:
            self.scanning = False
            self.mainWindow.statusBar1.SetStatusText('', 2)
            self.mainWindow.btnRefresh.SetLabel('Refresh List')
            self.mainWindow.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
            self.scanThread.join()
            self.mainWindow.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

    def returnHosts(self, hosts):
        self.mainWindow.statusBar1.SetStatusText('', 2)
        self.scanning = False
        self.mainWindow.btnRefresh.SetLabel('Refresh List')
        print hosts

    def createNewAdapter(self, event):
        addDevicedlg = AddController(self.adapterNameDict, self.mainWindow)
        if addDevicedlg.ShowModal() == wx.ID_OK:
            ipAddr = addDevicedlg.window.txtIP.GetValue()
            name = addDevicedlg.window.txtName.GetValue()

            # create device
            tunTap = API.AtumsoftGeneric.AtumsoftGeneric()  # isVirtual=True, iface='enp0s25')
            tunTap.createTunTapAdapter(name=name, ipAddress=ipAddr)
            tunTap.openTunTap()
            self.tunTapDict[name] = tunTap

            # add to list
            index = self.mainWindow.lstAdapters.GetItemCount()
            self.mainWindow.lstAdapters.InsertStringItem(index, str(index+1))
            self.mainWindow.lstAdapters.SetStringItem(index, 1, name)
            self.mainWindow.lstAdapters.SetStringItem(index, 2, ipAddr)
            self.mainWindow.lstAdapters.SetStringItem(index, 3, 'False')

            self.adapterNameDict[name] = True


    # Separate thread funcs --------------------------------------------------------------------------------------------
    def _scan(self):
        hosts = API.AtumsoftUtils.findHosts(self.networkIfaceIP)
        wx.CallAfter(self.returnHosts, hosts=hosts)


# Helper functions to check for admin privileges on run ================================================================
def checkForAdmin():
    try:
        is_admin = os.getuid() == 0
        if not is_admin:
            print "Script not started as root. Running sudo.."
            args = ['sudo', sys.executable] + sys.argv + [os.environ]
            # the next line replaces the currently-running process with the sudo
            os.execlpe('gksudo', *args)

    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            runAsAdmin()


def runAsAdmin(cmdLine=None, wait=True):

    if os.name != 'nt':
        raise RuntimeError, "This function is only implemented on Windows."

    import win32api, win32con, win32event, win32process
    from win32com.shell.shell import ShellExecuteEx
    from win32com.shell import shellcon

    python_exe = sys.executable

    if cmdLine is None:
        cmdLine = [python_exe] + sys.argv
    elif type(cmdLine) not in (types.TupleType,types.ListType):
        raise ValueError, "cmdLine is not a sequence."
    cmd = '"%s"' % (cmdLine[0],)
    params = " ".join(['"%s"' % (x,) for x in cmdLine[1:]])
    cmdDir = ''
    showCmd = win32con.SW_SHOWNORMAL
    #showCmd = win32con.SW_HIDE
    lpVerb = 'runas'  # causes UAC elevation prompt.

    # print "Running", cmd, params

    # ShellExecute() doesn't seem to allow us to fetch the PID or handle
    # of the process, so we can't get anything useful from it. Therefore
    # the more complex ShellExecuteEx() must be used.

    # procHandle = win32api.ShellExecute(0, lpVerb, cmd, params, cmdDir, showCmd)

    procInfo = ShellExecuteEx(nShow=showCmd,
                              fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                              lpVerb=lpVerb,
                              lpFile=cmd,
                              lpParameters=params)

    if wait:
        procHandle = procInfo['hProcess']
        obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
        rc = win32process.GetExitCodeProcess(procHandle)
        #print "Process handle %s returned code %s" % (procHandle, rc)
    else:
        rc = None

    return rc