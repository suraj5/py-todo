import wx
from db import DBA
from ui.main import MainFrame, APP_TITLE, APP_VERSION

if __name__ == '__main__':
    print 'Starting %s v%s' % (APP_TITLE, APP_VERSION)
    app = wx.PySimpleApp()
    MainFrame(DBA()).Show(True)
    app.MainLoop()