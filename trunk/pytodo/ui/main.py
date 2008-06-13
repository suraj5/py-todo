import wx
from task import AddEditTask

APP_TITLE = 'PyTodo'
APP_VERSION = '0.1'

class MainFrame(wx.Frame):
    def __init__(self, db):
        self.db = db
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
        self.add_btn = wx.Button(self.panel, label='Add Task')
        self.add_btn.Bind(wx.EVT_BUTTON, self.OnAddTask)
        self.edit_btn = wx.Button(self.panel, label='Edit Task')
        self.remove_btn = wx.Button(self.panel, label='Remove Task')

        # disable edit and remove buttons by default
        self.edit_btn.Enable(False)
        self.remove_btn.Enable(False)

        controls = wx.BoxSizer(wx.HORIZONTAL)
        controls.AddF(self.add_btn, def_flags)
        controls.AddF(self.edit_btn, def_flags)
        controls.AddF(self.remove_btn, wx.SizerFlags(1).Expand())

        self.sizer.AddF(controls, wx.SizerFlags(0).Expand().Border(wx.BOTTOM, 10))

        # task list
        self.tasks = wx.ListCtrl(self.panel, style=wx.BORDER_SUNKEN|wx.LC_REPORT)
        self.sizer.Add(self.tasks, proportion=1, flag=wx.EXPAND)
    
    def OnAddTask(self, event):
        task_dlg = AddEditTask(self)
        task_dlg.ShowModal()

    def OnClose(self, event):
        print 'Cleaning up...'
        self.Destroy()