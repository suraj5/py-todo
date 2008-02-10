import pygtk
pygtk.require('2.0')
import gtk, gobject, logging
from datetime import datetime
from db.db import Database, Task

DB = Database()
SHOW_COMPLETED = False

# setup the logger
level = logging.DEBUG
f = '%(asctime)s: %(levelname)s; %(name)s (%(lineno)d) %(message)s'

LOG = logging.getLogger('PyTodo')
LOG.setLevel(level)

ch = logging.StreamHandler()
ch.setLevel(level)

formatter = logging.Formatter(f)
ch.setFormatter(formatter)
LOG.addHandler(ch)

class PyTodo:
  def __init__(self):
    DB.check_tables()
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title('PyTodo')
    self.window.set_border_width(5)
    self.window.connect('delete_event', self.destroy)
    self.__add_controls()

    # restore size and position preferences
    height, width, top, left = DB.get_size_and_pos()
    self.window.resize(width, height)
    self.window.move(left, top)

    # restore the setting for whether or not completed tasks are to be shown
    SHOW_COMPLETED = DB.get_setting('show_completed') == 'True'
    self.show_completed_button.set_active(SHOW_COMPLETED)

    self.window.show_all()

  def __add_controls(self):
    self.vbox = gtk.VBox(False, 5)

    self.button_box = gtk.HBox(True, 5)

    # add task button
    self.add_task_button = gtk.Button('New Task', gtk.STOCK_ADD)
    self.add_task_button.connect('clicked', self.add_task, None)
    self.button_box.pack_start(self.add_task_button, True, True, 0)

    # edit task button
    #self.edit_task_button = gtk.Button('Edit Task', gtk.STOCK_EDIT)
    #self.edit_task_button.connect('clicked', self.edit_task, None)
    #self.button_box.pack_start(self.edit_task_button, True, True, 0)

    # delete task button
    self.delete_task_button = gtk.Button('Delete Task', gtk.STOCK_DELETE)
    self.delete_task_button.connect('clicked', self.delete_task, None)
    self.button_box.pack_start(self.delete_task_button, True, True, 0)

    # quit task button
    self.quit_task_button = gtk.Button('Quit', gtk.STOCK_QUIT, None)
    self.quit_task_button.connect('clicked', self.destroy)
    self.button_box.pack_start(self.quit_task_button, True, True, 0)

    self.vbox.pack_start(self.button_box, False, False, 0)

    # show/hide completed tasks button
    self.show_completed_button = gtk.CheckButton('Show completed tasks')
    self.show_completed_button.connect('toggled', self.save_show_completed, None)
    self.vbox.pack_start(self.show_completed_button, False, False, 0)

    # task list
    self.tree_scroller = gtk.ScrolledWindow()
    self.tree_scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.vbox.pack_start(self.tree_scroller, True, True, 0)

    self.treeview = TaskList.make_view(Tasks.get_model())
    self.tree_scroller.add(self.treeview)

    #self.tree_scroller.show()
    self.window.add(self.vbox)

    # create a system tray icon
    self.tray_icon = gtk.StatusIcon()
    self.tray_icon.set_from_stock(gtk.STOCK_APPLY)
    self.tray_icon.set_tooltip('PyTodo')
    #self.tray_icon.set_blinking(True)
    self.tray_icon.connect('activate', self.tray_icon_clicked, None)
    self.tray_icon.set_visible(True)

  def add_task(self, widget, event, data=None):
    LOG.info('adding task')
    Tasks.add_task()

  def edit_task(self, widget, event, data=None):
    LOG.info('editing task')

  def toggle_task_complete(self, widget, path, data=None):
    LOG.info('toggling task complete')
    LOG.info('Path: %s' % path)
    widget.set_active(not widget.get_active())

  def delete_task(self, widget, event, data=None):
    LOG.info('deleting task')

  def tray_icon_clicked(self, widget, event, data=None):
    LOG.info('Tray icon clicked')
    if self.window.is_active():
      self.window.iconify()
      self.window.set_skip_taskbar_hint(True)
    else:
      self.window.set_skip_taskbar_hint(False)
      self.window.present()

  def save_show_completed(self, widget, event, data=None):
    LOG.info('setting show completed to %s' % self.show_completed_button.get_active())
    DB.set_setting('show_completed', self.show_completed_button.get_active())

  def destroy(self, widget, event=None, data=None):
    self.__save_settings()
    DB.save_settings()

    self.tray_icon.set_visible(False)

    gtk.main_quit()
    return False

  def __save_settings(self):
    width, height = self.window.get_size()
    DB.set_setting('height', height)
    DB.set_setting('width', width)

    left, top = self.window.get_position()
    DB.set_setting('top', top)
    DB.set_setting('left', left)
    
class TasksModel:
  def __init__(self):
    self.treestore = gtk.TreeStore(gobject.TYPE_INT, 
                                    gobject.TYPE_STRING, 
                                    gobject.TYPE_STRING, 
                                    gobject.TYPE_BOOLEAN)
                                    
    # retrieve tasks from the database
    tasks = DB.get_all_tasks()
    for t in tasks:
      print SHOW_COMPLETED, t.complete, (not SHOW_COMPLETED and not t.complete)
      if (not SHOW_COMPLETED and not t.complete) or SHOW_COMPLETED:
        parent = self.treestore.append(None, [t.id,
                                               t.description, 
                                               t.date_due, 
                                               t.complete])
        self.__load_children(t, parent)
        
  def __load_children(self, task, parent):
    for t in task.children:
      if (not SHOW_COMPLETED and not t.complete) or SHOW_COMPLETED:
        piter = self.treestore.append(parent, [t.id,
                                                t.description, 
                                                t.date_due, 
                                                t.complete])

  def get_model(self):
    if self.treestore:
      return self.treestore
    else:
      return None
      
  def add_task(self, parent=None):
    new_id = DB.add_task()
    self.treestore.append(parent, [new_id,
                                    '',
                                    datetime.now(),
                                    False])

    return self.get_model()

class TaskListModel:
  def make_view(self, model):
    self.view = gtk.TreeView(model)

    self.desc_renderer = gtk.CellRendererText()
    self.desc_renderer.set_property('editable', True)
    self.desc_renderer.connect('edited', self.description_edited_cb, model)

    self.due_renderer = gtk.CellRendererText()
    self.due_renderer.set_property('editable', True)
    self.due_renderer.connect('edited', self.due_date_edited_cb, model)

    self.complete_renderer = gtk.CellRendererToggle()
    self.complete_renderer.set_property('activatable', True)
    self.complete_renderer.connect( 'toggled', self.completed_toggled_cb, model)

    self.column0 = gtk.TreeViewColumn('Task', self.desc_renderer, text=1)
    self.column0.set_resizable(True)
    self.column0.set_min_width(150)
    
    self.column1 = gtk.TreeViewColumn('Due', self.due_renderer, text=2)
    self.column1.set_min_width(70)
    self.column1.set_max_width(100)
    self.column1.set_resizable(True)

    self.column2 = gtk.TreeViewColumn(' ', self.complete_renderer)
    self.column2.set_resizable(True)
    #self.column2.set_max_width(30)
    self.column2.add_attribute(self.complete_renderer, 'active', 3)

    self.view.append_column(self.column2)
    self.view.append_column(self.column0)
    self.view.append_column(self.column1)

    return self.view
    
  def description_edited_cb(self, cell, path, new_value, model):
    print "Change '%s' to '%s'" % (model[path][1], new_value)
    model[path][1] = new_value
    DB.edit_task(model[path])
    return
    
  def due_date_edited_cb(self, cell, path, new_value, model):
    print "Change '%s' to '%s'" % (model[path][2], new_value)
    model[path][2] = new_value
    DB.edit_task(model[path])
    return
    
  def completed_toggled_cb(self, cell, path, model):
    print "Toggle '%s' to: %s" % (model[path][3], not model[path][3],)
    model[path][3] = not model[path][3]
    DB.edit_task(model[path])
    return

def main():
  gtk.main()
  return 0

if __name__ == '__main__':
  Tasks = TasksModel()
  TaskList = TaskListModel()
  pyTodo = PyTodo()
  main()