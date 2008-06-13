import wx

class AddEditTask(wx.Dialog):
    def __init__(self, parent, task=None):
        super(AddEditTask, self).__init__(parent, title='Add New Task')
        
        # panels and sizers
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(psizer)

        self.panel = wx.Panel(self)
        psizer.AddF(self.panel, wx.SizerFlags(1).Expand().Border(wx.ALL, 10))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)
        
        bottom_bdr = wx.SizerFlags(0).Expand().Border(wx.BOTTOM, 5)
        
        # task name
        name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        name_sizer.Add(wx.StaticText(self.panel, label='Task:'), flag=wx.ALIGN_CENTER_VERTICAL)
        name_sizer.AddSpacer((5,5))
        self.task_name = wx.TextCtrl(self.panel)
        name_sizer.Add(self.task_name, proportion=1, flag=wx.EXPAND)
        self.sizer.AddF(name_sizer, bottom_bdr)