import pygtk
pygtk.require('2.0')
import gtk, logging
from db.db import Database

DB = Database()

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

    # create a system tray icon
    self.tray_icon = gtk.StatusIcon()
    self.tray_icon.set_from_stock(gtk.STOCK_HOME)
    self.tray_icon.set_tooltip('PyTodo')
    self.tray_icon.set_blinking(True)
    self.tray_icon.connect('activate', self.tray_icon_clicked, None)
    #self.tray_icon.show()

    # restore size and position preferences
    height, width, top, left = DB.get_size_and_pos()
    self.window.resize(width, height)
    self.window.move(left, top)

    # restore the setting for whether or not completed tasks are to be shown
    sc = DB.get_setting('show_completed') == 'True'
    self.show_completed_button.set_active(sc)

    self.window.show_all()

  def __add_controls(self):
    self.vbox = gtk.VBox(False, 5)

    self.button_box = gtk.HBox(True, 5)

    # add task button
    self.add_task_button = gtk.Button('New Task', gtk.STOCK_ADD)
    self.add_task_button.connect('clicked', self.add_task, None)
    self.button_box.pack_start(self.add_task_button, True, True, 0)

    # edit task button
    self.edit_task_button = gtk.Button('Edit Task', gtk.STOCK_EDIT)
    self.edit_task_button.connect('clicked', self.edit_task, None)
    self.button_box.pack_start(self.edit_task_button, True, True, 0)

    # delete task button
    self.delete_task_button = gtk.Button('Delete Task', gtk.STOCK_DELETE)
    self.delete_task_button.connect('clicked', self.delete_task, None)
    self.button_box.pack_start(self.delete_task_button, True, True, 0)

    # quit task button
    self.quit_task_button = gtk.Button('Quit', gtk.STOCK_QUIT, None)
    self.quit_task_button.connect('clicked', self.destroy)
    self.button_box.pack_start(self.quit_task_button, True, True, 0)

    self.vbox.pack_start(self.button_box, False, False, 0)

    # task list
    self.tree_scroller = gtk.ScrolledWindow()
    self.tree_scroller.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.vbox.pack_start(self.tree_scroller, True, True, 0)

    # create the TreeStore
    self.treestore = gtk.TreeStore(str, str, 'gboolean')

    self.treeview = gtk.TreeView(self.treestore)

    self.tree_scroller.add(self.treeview)

    # show/hide completed tasks button
    self.show_completed_button = gtk.ToggleButton('Show completed tasks')
    self.show_completed_button.connect('toggled', self.save_show_completed, None)
    self.vbox.pack_end(self.show_completed_button, False, False, 0)

    self.tree_scroller.show()
    self.window.add(self.vbox)

  def add_task(self, widget, event, data=None):
    LOG.info('adding task')

  def edit_task(self, widget, event, data=None):
    LOG.info('editing task')

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
    gtk.main_quit()
    return False

  def __save_settings(self):
    width, height = self.window.get_size()
    DB.set_setting('height', height)
    DB.set_setting('width', width)

    left, top = self.window.get_position()
    DB.set_setting('top', top)
    DB.set_setting('left', left)

def main():
  gtk.main()
  return 0

if __name__ == '__main__':
  pyTodo = PyTodo()
  main()