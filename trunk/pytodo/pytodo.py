import wx
from ui.main import MainFrame, APP_TITLE, APP_VERSION

if __name__ == '__main__':
    print 'Starting %s v%s' % (APP_TITLE, APP_VERSION)
    app = wx.PySimpleApp()
    MainFrame().Show(True)
    app.MainLoop()