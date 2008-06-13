import wx

priorities = (
    ('Urgent'),
    ('Important'),
    ('Normal'),
    ('Low'),
    ('Very low'),
)

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
        detail_sizer = wx.FlexGridSizer(hgap=5, vgap=5, rows=2, cols=4)
        detail_sizer.Add(wx.StaticText(self.panel, label='Task:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.task_name = wx.TextCtrl(self.panel)
        detail_sizer.Add(self.task_name, proportion=3, flag=wx.EXPAND)
        
        # priority
        detail_sizer.Add(wx.StaticText(self.panel, label='Priority:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.priority = wx.ComboBox(self.panel, choices=priorities)
        detail_sizer.Add(self.priority, proportion=1, flag=wx.EXPAND)
        
        # due
        detail_sizer.Add(wx.StaticText(self.panel, label='Due by:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.due_by = wx.DatePickerCtrl(self.panel, style=wx.DP_DROPDOWN|wx.DP_ALLOWNONE)
        detail_sizer.Add(self.due_by)
        
        self.sizer.AddF(detail_sizer, bottom_bdr)
        
        # description
        self.sizer.Add(wx.StaticText(self.panel, label='Description:'))
        self.description = wx.TextCtrl(self.panel, style=wx.BORDER_SUNKEN|wx.TE_MULTILINE|wx.TE_AUTO_SCROLL)
        self.sizer.Add(self.description, proportion=1, flag=wx.EXPAND)
        
        # buttons
        std_btns = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        psizer.AddF(std_btns, wx.SizerFlags(0).Expand().Border(wx.RIGHT|wx.BOTTOM, 10))