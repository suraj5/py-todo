import wx
import menus
import utils
from task import AddEditTask

APP_TITLE = 'PyTodo'
APP_VERSION = '0.1'

class MainFrame(wx.Frame):
    """
    This is the main screen for this program.  It presents a list of tasks and
    a few controls for adding, editing, and removing tasks.
    """
    
    def __init__(self, db):
        self.db = db
        super(MainFrame, self).__init__(None, title=APP_TITLE)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.build_gui()
        
        # hide the program by default
        if self.tray_icon.IsIconInstalled():
            pass
   
    def build_gui(self):
        # icons
        self.SetIcon(utils.get_icon('todo'))
        self.tray_icon = wx.TaskBarIcon()
        self.tray_icon.SetIcon(utils.get_icon('tray16'))
        
        self.tray_icon.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnToggleState)
        
        # add a menu bar
        self.statusbar = self.CreateStatusBar()
        self.SetMenuBar(menus.buildMenuBar(self, self.get_menus()))
        self.GetMenuBar().FindItemById(wx.ID_OPEN).Enable(False)
        self.GetMenuBar().FindItemById(wx.ID_CLOSE).Enable(False)
        
        # add a toolbar
        self.toolbar = self.CreateToolBar()
        self.toolbar.AddSimpleTool(wx.ID_NEW, utils.get_bmp('add'), 'Add New Task', 'Create a new task')
        self.toolbar.AddSimpleTool(wx.ID_OPEN, utils.get_bmp('edit'), 'Edit Task', 'Edit the selected task')
        self.toolbar.AddSimpleTool(wx.ID_CLOSE, utils.get_bmp('remove'), 'Remove Task', 'Remove the selected task')
        
        # disable the edit and remove buttons by default
        self.toolbar.EnableTool(wx.ID_OPEN, False)
        self.toolbar.EnableTool(wx.ID_CLOSE, False)
        
        # panels and sizers
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(psizer)

        self.panel = wx.Panel(self)
        psizer.AddF(self.panel, wx.SizerFlags(1).Expand().Border(wx.ALL, 10))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.sizer)

        # flags
        def_flags = wx.SizerFlags(1).Expand().Border(wx.RIGHT, 5)
        szr_flags = wx.SizerFlags(0).Expand().Border(wx.BOTTOM, 5)

        # control buttons
        #self.add_btn = wx.Button(self.panel, id=wx.ID_NEW, label='Add Task')
        #self.add_btn.Bind(wx.EVT_BUTTON, self.OnAddTask)
        #self.edit_btn = wx.Button(self.panel, id=wx.ID_OPEN, label='Edit Task')
        #self.remove_btn = wx.Button(self.panel, id=wx.ID_CLOSE, label='Remove Task')

        # disable edit and remove buttons by default
        #self.edit_btn.Enable(False)
        #self.remove_btn.Enable(False)

        #controls = wx.BoxSizer(wx.HORIZONTAL)
        #controls.AddF(self.add_btn, def_flags)
        #controls.AddF(self.edit_btn, def_flags)
        #controls.AddF(self.remove_btn, wx.SizerFlags(1).Expand())

        #self.sizer.AddF(controls, szr_flags)
        
        # quick filter
        search = wx.BoxSizer(wx.HORIZONTAL)
        search.Add(wx.StaticText(self.panel, label='Filter: '), flag=wx.ALIGN_CENTER_VERTICAL)
        self.filter = wx.TextCtrl(self.panel)
        search.Add(self.filter, proportion=1, flag=wx.EXPAND)
        
        self.sizer.AddF(search, szr_flags)

        # task list
        self.tasks = wx.TreeCtrl(self.panel, style=wx.BORDER_SUNKEN|wx.TR_HIDE_ROOT)
        self.sizer.Add(self.tasks, proportion=1, flag=wx.EXPAND)
        
        self.root = self.tasks.AddRoot('All Tasks')
    
    def get_menus(self):
        """
        This method is a stripped-down, super easy way to create a menubar, using
        my menus.py utility script.
        """
        
        return [
            ('File', [
                ('New task...\tCtrl+N', 'Add a new task', self.OnAddTask, wx.ID_NEW),
                ('Edit task...\tCtrl+E', 'Edit the selected task', None, wx.ID_OPEN),
                ('Remove task...\tDel', 'Remove the selected task', None, wx.ID_CLOSE),
                (None, ),
                ('&Quit\tCtrl+Q', 'Close down this program', self.OnClose, wx.ID_EXIT)
                ]),
            ('Help', [
                ('About %s...\tCtrl+H' % APP_TITLE, 'Learn a little about this program', self.OnAbout, wx.ID_ABOUT),
                ]),
        ]
    
    def OnToggleState(self, event):
        print event
    
    def OnAddTask(self, event):
        task_dlg = AddEditTask(self)
        task_dlg.ShowModal()
    
    def OnAbout(self, event):
        """
        Show a silly little about box for the program.
        """
        description = "%s is a pet project written by Josh VanderLinden using Python, wxPython, and MetaKit. Josh created this program mostly just for fun, but also to learn more about the three things mentioned in the last sentence." % APP_TITLE
        try:
            about = wx.AboutDialogInfo()
        except AttributeError, err:
            # older version of python
            wx.MessageBox(description,
                          'About This Program',
                          wx.OK|wx.ICON_INFORMATION)
        else:
            #about.SetIcon(utils.get_icon('scriptures'))
            about.SetName(APP_TITLE)
            about.SetVersion(APP_VERSION)
            about.SetDescription(description)
            about.SetCopyright("Copyright 2008 Josh VanderLinden")
            about.SetDevelopers(["Josh VanderLinden"])
            about.SetWebSite('http://code.google.com/p/py-todo/')
            wx.AboutBox(about)

    def OnClose(self, event):
        print 'Cleaning up...'
        self.Destroy()
