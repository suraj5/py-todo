import wx
import re
import datetime

priorities = (
    ('Urgent'),
    ('Important'),
    ('Normal'),
    ('Low'),
    ('Very low'),
)

class DateTimeCtrl(wx.PyPanel):
    """
    This is a custom control that combines a date picker and a combobox to choose or enter times.
    """
    
    re_time = re.compile('(\d{1,2}):(\d{2}) (\w{2})')
    
    def __init__(self, parent, value=None):
        super(DateTimeCtrl, self).__init__(parent)
    
        # make a list of possible times
        times = []
        hours = [12] + range(1,12)
        for a in ['AM', 'PM']:
            for hour in hours:
                for m in [0, 15, 30, 45]:
                    times.append('%i:%02i %s' % (hour, m, a))
    
        self.date = wx.DatePickerCtrl(self, style=wx.DP_DROPDOWN|wx.DP_ALLOWNONE, pos=(0, 0), size=(100, 25))
        self.time = wx.ComboBox(self, choices=times, pos=(105, 0), size=(100, 25))
        self.SetValue(value)

    def GetValue(self):
    	date = self.date.GetValue()
        time = self.time.GetValue()
        m = self.re_time.match(time)

        if not date:
            raise ValueError('Invalid date!')
        elif not m or (m and len(m.groups()) != 3):
            raise ValueError('Invalid time!')
        else:
            hour, minute, ampm = m.groups()
            hour, minute = int(hour), int(minute)
            if ampm.upper() == 'PM':
                hour += 12
            value = datetime.datetime(date.Year, date.Month + 1, date.Day, hour, minute)
        return value
    
    def SetValue(self, value):
        if value:
            self.date.SetValue(value)
            self.time.SetValue(value.strftime('%I:%M %p'))

class AddEditTask(wx.Dialog):
    def __init__(self, parent, task=None):
    	if task:
    	    action = 'Edit'
    	else:
    	    action = 'Add'
    	
        super(AddEditTask, self).__init__(parent, title='%s New Task' % action, style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.DIALOG_MODAL)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.SetMinSize((515, 230))
        
        # panels and sizers
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(psizer)

        self.panel = wx.Panel(self)
        psizer.AddF(self.panel, wx.SizerFlags(1).Expand().Border(wx.ALL, 10))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)
        
        bottom_bdr = wx.SizerFlags(0).Expand().Border(wx.BOTTOM, 5)
        
        detail_sizer = wx.FlexGridSizer(hgap=5, vgap=5, rows=2, cols=4)
        detail_sizer.AddGrowableCol(1, proportion=1)
        #detail_sizer.AddGrowableCol(3, proportion=1)
        
        # task name
        detail_sizer.Add(wx.StaticText(self.panel, label='Task:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.task_name = wx.TextCtrl(self.panel)
        detail_sizer.Add(self.task_name, flag=wx.EXPAND)
        
        # priority
        detail_sizer.Add(wx.StaticText(self.panel, label='Priority:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.priority = wx.ComboBox(self.panel, value='Normal', choices=priorities)
        detail_sizer.Add(self.priority, flag=wx.EXPAND)
        
        # tags
        detail_sizer.Add(wx.StaticText(self.panel, label='Tags:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.tags = wx.TextCtrl(self.panel)
        detail_sizer.Add(self.tags, flag=wx.EXPAND)
        
        # due
        detail_sizer.Add(wx.StaticText(self.panel, label='Due by:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.due_by = DateTimeCtrl(self.panel)
        detail_sizer.Add(self.due_by, flag=wx.EXPAND)
        detail_sizer.SetItemMinSize(self.due_by, (205, 25))
        
        self.sizer.Add(detail_sizer, flag=wx.EXPAND)
        
        # description
        self.sizer.Add(wx.StaticText(self.panel, label='Description:'))
        self.description = wx.TextCtrl(self.panel, style=wx.BORDER_SUNKEN|wx.TE_MULTILINE|wx.TE_AUTO_SCROLL)
        self.sizer.Add(self.description, proportion=1, flag=wx.EXPAND)
        
        # buttons
        std_btns = self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL)
        self.complete = wx.CheckBox(self, label='Complete', style=wx.CHK_3STATE|wx.CHK_ALLOW_3RD_STATE_FOR_USER)
        std_btns.Insert(0, self.complete, flag=wx.ALIGN_CENTER_VERTICAL)
        psizer.AddF(std_btns, wx.SizerFlags(0).Expand().Border(wx.LEFT|wx.RIGHT|wx.BOTTOM, 10))
        
    def OnClose(self, event):
        print self.due_by.GetValue()
        self.Destroy()