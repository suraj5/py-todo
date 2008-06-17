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
        super(MainFrame, self).__init__(None, title=APP_TITLE)#, style=wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL|wx.FRAME_NO_TASKBAR)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_ICONIZE, self.OnIconize)
        
        self.build_gui()
   
    def build_gui(self):
        self.SetMinSize((250, 300))
        
        # icons
        self.SetIcon(utils.get_icon('todo'))
        self.tray_icon = wx.TaskBarIcon()
        self.tray_icon.SetIcon(utils.get_icon('tray16'))
        
        self.tray_icon.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.OnDeIconize)
        self.tray_icon.Bind(wx.EVT_TASKBAR_RIGHT_UP, self.OnTrayMenu)
        
        # add a menu bar
        self.statusbar = self.CreateStatusBar()
        self.SetMenuBar(menus.buildMenuBar(self, self.get_menus()))
        self.GetMenuBar().FindItemById(wx.ID_OPEN).Enable(False)
        self.GetMenuBar().FindItemById(wx.ID_CLOSE).Enable(False)
        
        # build a menu for the tray icon
        self.tray_menu = wx.Menu()
        self.tray_menu.Append(wx.ID_NEW, 'New task...')
        self.tray_menu.Append(wx.ID_ABOUT, 'About PyTodo...')
        self.tray_menu.Append(wx.ID_EXIT, 'Quit')
        
        # add a toolbar
        self.toolbar = self.CreateToolBar(style=wx.TB_HORIZONTAL|wx.NO_BORDER)
        self.toolbar.AddSimpleTool(wx.ID_NEW, utils.get_bmp('add'), 'Add New Task', 'Create a new task')
        self.toolbar.AddSimpleTool(wx.ID_OPEN, utils.get_bmp('edit'), 'Edit Task', 'Edit the selected task')
        self.toolbar.AddSimpleTool(wx.ID_CLOSE, utils.get_bmp('remove'), 'Remove Task', 'Remove the selected task')
        self.toolbar.AddSeparator()
        self.toolbar.AddControl(wx.StaticText(self.toolbar, label='Filter: '))
        self.filter = wx.TextCtrl(self.toolbar)
        self.toolbar.AddControl(self.filter)
        
        # disable the edit and remove buttons by default
        self.toolbar.EnableTool(wx.ID_OPEN, False)
        self.toolbar.EnableTool(wx.ID_CLOSE, False)
        
        # task list
        self.tasks = wx.TreeCtrl(self, style=wx.BORDER_SUNKEN|wx.TR_HIDE_ROOT)
        
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
                ('&Quit\tCtrl+Q', 'Close down this program', self.OnExit, wx.ID_EXIT)
                ]),
            ('Help', [
                ('About %s...\tCtrl+H' % APP_TITLE, 'Learn a little about this program', self.OnAbout, wx.ID_ABOUT),
                ]),
        ]
    
    def OnDeIconize(self, event):
        self.Show(True)
        self.Iconize(False)
        self.Raise()
    
    def OnIconize(self, event, force=False):
        # this seems a little counter-intuitive, but it works.
        if self.IsIconized() or force:
            # minimize the application
            self.Iconize(True)
            
            # remove the button from the task bar
            self.Hide()
        
    def OnTrayMenu(self, event):
        """
        Event handler to display the tray icon's menu
        """
        self.PopupMenu(self.tray_menu)
    
    def OnAddTask(self, event):
        """
        Event handler to add a new task
        """
        task_dlg = AddEditTask(self)
        task_dlg.ShowModal()
    
    def OnAbout(self, event):
        """
        Show a silly little about box for the program.
        """
        description = """%s is a pet project written by Josh VanderLinden using
Python, wxPython, and MetaKit. Josh created this program
mostly just for fun, but also to learn more about the three
things mentioned in the last sentence.""" % APP_TITLE
        try:
            about = wx.AboutDialogInfo()
        except AttributeError, err:
            # older version of python
            wx.MessageBox(description,
                          'About This Program',
                          wx.OK|wx.ICON_INFORMATION)
        else:
            about.SetIcon(utils.get_icon('tray'))
            about.SetName(APP_TITLE)
            about.SetVersion(APP_VERSION)
            about.SetDescription(description)
            about.SetCopyright("Copyright 2008 Josh VanderLinden")
            about.SetDevelopers(["Josh VanderLinden"])
            about.SetWebSite('http://code.google.com/p/py-todo/')
            wx.AboutBox(about)

    def OnClose(self, event):
        """
        Event handler to catch the signal to close the program and send it to
        the system tray.
        """
        self.OnIconize(event, True)
    
    def OnExit(self, event):
        """
        Event handler to handle program cleanup and shutdown
        """
        
        print 'Cleaning up...'
        self.Destroy()
