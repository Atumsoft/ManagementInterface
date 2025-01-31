import ast
import json
import random

import thread

import subprocess

import time
from mainView import MainFrame
from CustomControlls import DiagController, AddController, ConnectController

from cStringIO import StringIO
import sys
import wx
import API
import threading
import requests
import _winreg as wr

import routesplice

sys.stdout = mystdout = StringIO()


class Controller:
    def __init__(self):
        # initialize view params
        self.mainWindow = MainFrame(None)
        self.mainWindow.timer1.Start(1000)
        self.mainWindow.statusBar1.SetStatusText('No connected Device', 0)

        self.mainWindow.lstAdapters.InsertColumn(0, 'Number', width=35)
        self.mainWindow.lstAdapters.InsertColumn(1, 'Name', width=100)
        self.mainWindow.lstAdapters.InsertColumn(2, 'IP Address', width=100)
        self.mainWindow.lstAdapters.InsertColumn(3, 'Capturing', width=wx.COL_WIDTH_AUTOSIZE)

        self.mainWindow.lstDevices.InsertColumn(0, 'Remote IP', width=100)
        self.mainWindow.lstDevices.InsertColumn(1, 'Virtual IP Address', width=100)
        self.mainWindow.lstDevices.InsertColumn(2, 'Virtual Mac Address', width=125)

        # setup bindings
        self.mainWindow.Bind(wx.EVT_MENU, self.showDiag, self.mainWindow.menuShowLog)
        self.mainWindow.Bind(wx.EVT_TIMER, self.update, self.mainWindow.timer1)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.createNewAdapter, self.mainWindow.btnCreate)
        self.mainWindow.Bind(wx.EVT_BUTTON, self.scan, self.mainWindow.btnRefresh)
        self.mainWindow.Bind(wx.EVT_CONTEXT_MENU, self.onRClick, self.mainWindow.lstDevices)
        self.mainWindow.Bind(wx.EVT_CLOSE, self.onClose)

        # class vars
        self.scanning = False
        self.tunTapDict = {}
        self.hostsDict = {}
        self.usedPorts = []
        self.RunningSocketList = []

        # networking vars
        self.networkGatewayIP, self.networkIface = API.AtumsoftUtils.findGateWay()
        self.networkIfaceIP = API.AtumsoftUtils.getIP(self.networkIface)

        # dictionaries to make sure names are unique
        self.adapterNameDict = {}

        thread.start_new_thread(API.AtumsoftServer.runConnectionServer, tuple(),{'runSocketServeronStart':True})

    def show(self):
        self.mainWindow.Show()

    def destroy(self):
        self.mainWindow.Destroy()

    def onClose(self, event):
        self.mainWindow.Hide()

    def showDiag(self, event):
        dlg = DiagController(mystdout,self.mainWindow)
        dlg.ShowModal()

    def exit(self):
        exit(0)

    def onRClick(self, event):
        if self.mainWindow.lstDevices.GetNextSelected(-1) < 0: return

        if not hasattr(self, 'popupID1'):
            self.popupID1 = wx.NewId()
            self.mainWindow.Bind(wx.EVT_MENU, self.onConnectClicked, id=self.popupID1)

        menu = wx.Menu()
        menuItemOne = menu.Append(self.popupID1, "connect to...")

        self.mainWindow.PopupMenu(menu)
        menu.Destroy()

    def onConnectClicked(self, event):
        currentItem = self.mainWindow.lstDevices.GetNextSelected(-1)
        dlg = ConnectController(self.mainWindow)

        dlg.lstAdapters.InsertColumn(0, 'Number', width=35)
        dlg.lstAdapters.InsertColumn(1, 'Name', width=100)
        dlg.lstAdapters.InsertColumn(2, 'IP Address', width=100)
        dlg.lstAdapters.InsertColumn(3, 'Capturing', width=wx.COL_WIDTH_AUTOSIZE)

        for itemIndex in xrange(self.mainWindow.lstAdapters.GetItemCount()):
            itemList = []
            for colIndex in xrange(self.mainWindow.lstAdapters.GetColumnCount()):
                itemList.append( self.mainWindow.lstAdapters.GetItem(itemIndex, colIndex) )

            # FIXME: I don't like hard coding in the column indexes
            index = dlg.lstAdapters.InsertItem(itemList[0])
            dlg.lstAdapters.SetItem(itemList[1])
            dlg.lstAdapters.SetItem(itemList[2])
            dlg.lstAdapters.SetItem(itemList[3])

        shownID = dlg.ShowModal()
        if shownID != wx.ID_CANCEL:
            if shownID == wx.ID_OPEN:
                self.createNewAdapter(generate=self.hostsDict[currentItem]['virtualIP'])
                print self.tunTapDict
                virtualAdapter = self.tunTapDict[len(self.tunTapDict)-1]

            elif shownID == wx.ID_OK:
                virtualAdapterIndex = dlg.selectedIndex
                virtualAdapter = self.tunTapDict.get(virtualAdapterIndex)

            remoteHost = self.hostsDict[currentItem]['hostIP']
            data = {virtualAdapter.ipAddress: virtualAdapter.macAddress}
            # print 'data: %s' % remoteHost

            port = 6000 + (len(self.RunningSocketList)*10)
            self.RunningSocketList.append(port)
            data.update({'port': port})

            r = requests.post('http://%s:5000/connect' % remoteHost, data=json.dumps(data))
            if r.status_code != 200: print 'error connecting to host at: %s\nStatus Code %s' % (remoteHost, r.status_code); return

            info = requests.get('http://%s:5000/getinfo' % remoteHost)
            info = info.json()


            # r = requests.post('http://%s:5000/openSocket' % remoteHost, data=str(newPort))
            # if r.status_code != 200: print 'error opening socket at address (%s, %s)' % (remoteHost, newPort)

            thread.start_new_thread(self._startCapturing, (virtualAdapter, info, remoteHost, port))

            # do windows routing commands for ips on same subnet
            time.sleep(5) # have to wait for windows to self populate routing table...
            tapDevNumDict = routesplice.spliceRouteTable()
            ifNum = tapDevNumDict.get(len(self.RunningSocketList))

            ipList = virtualAdapter.ipAddress.split('.')
            ipList[3] = '0'
            gateWayIP = '.'.join(ipList)
            cleanupCommand = 'route delete %s' % gateWayIP
            subprocess.call(cleanupCommand)

            addCommand = 'route add %s mask 255.255.255.255 0.0.0.0 if %s' % (info.keys()[0], ifNum)
            subprocess.call(addCommand)

    def update(self, event):
        if not self.scanning: return

        if len(self.mainWindow.statusBar1.GetStatusText(2)) >= len('scanning...'):
            self.mainWindow.statusBar1.SetStatusText('scanning', 2)
        else:
            self.mainWindow.statusBar1.SetStatusText(self.mainWindow.statusBar1.GetStatusText(2) + '.', 2)

    def scan(self, event):
        if not self.scanning:
            self.mainWindow.lstDevices.DeleteAllItems()

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
        if not hosts: return

        # parse host data
        # FIXME: code set up for assuming only one virtual adapter on remote at the moment
        print 'hosts found: %s' % hosts
        for index, remoteIP in enumerate(hosts.keys()):
            virtualIP = hosts[remoteIP].keys()[0]
            virtualMAC = hosts[remoteIP][virtualIP]

            # Add host to list
            index = self.mainWindow.lstDevices.GetItemCount()
            self.mainWindow.lstDevices.InsertStringItem(index, remoteIP)
            self.mainWindow.lstDevices.SetStringItem(index, 1, virtualIP)
            self.mainWindow.lstDevices.SetStringItem(index, 2, virtualMAC)

            # add host to dict
            self.hostsDict[index] = {
                'hostIP'    : remoteIP,
                'virtualIP' : virtualIP,
                'virtualMAC': virtualMAC,
            }

    def createNewAdapter(self, event=None, generate=''):
        addDevicedlg = AddController(self.adapterNameDict, self.mainWindow)

        if generate:
            # generate a random IP address in the same subnet as the detected device
            ipAddrList = generate.split('.')
            ipToChange = int(ipAddrList.pop(3))
            allowedValues = range(0,255)
            allowedValues.remove(ipToChange)
            newIP = random.choice(allowedValues)

            ipAddrList.append(str(newIP))
            ipAddr = '.'.join(ipAddrList)
            name = 'adapter' + str(len(self.tunTapDict))
        else:
            shownID = addDevicedlg.ShowModal()
            if shownID == wx.ID_OK:
                ipAddr = addDevicedlg.window.txtIP.GetValue()
                name = addDevicedlg.window.txtName.GetValue()
            elif shownID == wx.ID_CANCEL:
                return

        # if this is the first adapter, make sure no other virtuals exist (potentially from a bad shutdown):
        if not self.tunTapDict:
            command = API.AtumsoftWindows.REMOVE_ALL_TAP_COMMAND
            proc = subprocess.Popen(command, stdout=subprocess.PIPE)
            print proc.communicate()[0]

        # create device
        self.mainWindow.SetCursor(wx.StockCursor(wx.CURSOR_WAIT))
        # thread.start_new_thread(self._createTunTap, (name, ipAddr)) # want this to be blocking for the moment

        # add to list
        index = self.mainWindow.lstAdapters.GetItemCount()
        self.mainWindow.lstAdapters.InsertStringItem(index, str(index+1))
        self.mainWindow.lstAdapters.SetStringItem(index, 1, name)
        self.mainWindow.lstAdapters.SetStringItem(index, 2, ipAddr)
        self.mainWindow.lstAdapters.SetStringItem(index, 3, 'False')

        self.adapterNameDict[name] = True
        self._createTunTap(name, ipAddr)

    def finishCreatingTunTap(self, tunTap):
        self.tunTapDict[self.mainWindow.lstAdapters.GetItemCount()-1] = tunTap
        # for some reason, windows closes tunTap devices on creation of a new device...
        # for tunTapDev in self.tunTapDict.values():
        #     tunTapDev.openTunTap()
        self.mainWindow.SetCursor(wx.StockCursor(wx.CURSOR_ARROW))

    def get_driver_name_from_guid(self, iface_guids):
        # iface_names = ['(unknown)' for i in range(len(iface_guids))]
        ifaceNameDict = {}
        reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}')
        for i in range(wr.QueryInfoKey(reg_key)[0]):
            subkey_name = wr.EnumKey(reg_key, i)
            try:
                reg_subkey = wr.OpenKey(reg_key, subkey_name)
                guid = wr.QueryValueEx(reg_subkey, 'NetCfgInstanceId')[0]
                try:
                    idx = iface_guids.index(guid)
                    ifaceNameDict[wr.QueryValueEx(reg_subkey, 'DriverDesc')[0]] = idx
                except ValueError:
                    pass
            except Exception, e:
                print e.message

        return ifaceNameDict

    # Separate thread funcs --------------------------------------------------------------------------------------------
    def _createTunTap(self, name, ipAddr):
        tunTap = API.AtumsoftGeneric.AtumsoftGeneric()  # isVirtual=True, iface='enp0s25')
        tunTap.createTunTapAdapter(name=name, ipAddress=ipAddr, existingNameList=self.adapterNameDict.keys())
        tunTap.openTunTap()
        for othertap in self.tunTapDict.values():
            try:
                othertap.openTunTap()
            except:
                pass

        # wx.CallAfter(self.finishCreatingTunTap, tunTap = tunTap)
        self.finishCreatingTunTap(tunTap)

    def _scan(self):
        hosts = API.AtumsoftUtils.findDevices([adapter.adapterInfo for adapter in self.tunTapDict.keys()])
        wx.CallAfter(self.returnHosts, hosts=hosts)

    def _startCapturing(self, virtualAdapter, info, host, port):
        virtualAdapter.startCapture(activeHosts={host: {'address': info}}, port=port)
