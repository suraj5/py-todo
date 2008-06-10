import wx

APP_TITLE = 'PyTodo'
APP_VERSION = '0.1'

class MainFrame(wx.Frame):
    def __init__(self):
        super(MainFrame, self).__init__(None, title=APP_TITLE)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # panels and sizers
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(psizer)

        self.panel = wx.Panel(self)
        psizer.AddF(self.panel, wx.SizerFlags(1).Expand().Border(wx.ALL, 10))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        # flags
        def_flags = wx.SizerFlags(1).Expand().Border(wx.RIGHT, 10)

        # control buttons
        self.addBtn = wx.Button(self.panel, label='Add Task')
        self.editBtn = wx.Button(self.panel, label='Edit Task')
        self.removeBtn = wx.Button(self.panel, label='Remove Task')

        # disable edit and remove buttons by default
        self.editBtn.Enable(False)
        self.removeBtn.Enable(False)

        controls = wx.BoxSizer(wx.HORIZONTAL)
        controls.AddF(self.addBtn, def_flags)
        controls.AddF(self.editBtn, def_flags)
        controls.AddF(self.removeBtn, wx.SizerFlags(1).Expand())

        self.sizer.AddF(controls, wx.SizerFlags(0).Expand().Border(wx.BOTTOM, 10))

        # task list
        self.tasks = wx.ListCtrl(self.panel, style=wx.BORDER_SUNKEN)
        self.sizer.Add(self.tasks, proportion=1, flag=wx.EXPAND)

    def OnClose(self, event):
        print 'Cleaning up...'
        self.Destroy()