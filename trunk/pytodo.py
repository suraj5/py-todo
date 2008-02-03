import pygtk
pygtk.require('2.0')
import gtk, logging
from pysqlite2 import dbapi2 as sqlite

# connect to the database
DB = sqlite.connect('pytodo.db')

# setup the logger
level = logging.DEBUG
f = '%(asctime)s - %(levelname)s - %(lineno)d - %(message)s'

LOG = logging.getLogger('PyTodo')
LOG.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
formatter = logging.Formatter(f)
ch.setFormatter(formatter)
LOG.addHandler(ch)

class PyTodo:
  def __init__(self):
    self.__check_tables()
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.set_title('PyTodo')
    self.window.set_border_width(5)
    self.window.connect('delete_event', self.destroy)
    self.__add_controls()
    
    # restore size and position preferences
    height, width, top, left = self.__get_size_and_pos()
    self.window.resize(width, height)
    self.window.move(left, top)
    
    # restore the setting for whether or not completed tasks are to be shown
    sc = self.__get_preference('show_completed') == 'True'
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
    
  def __check_tables(self):
    query = """
    create table if not exists tasks (
      id integer primary key autoincrement, 
      parent_id integer null,
      description text not null,
      complete boolean default false,
      date_created datetime default CURRENT_TIMESTAMP,
      date_due datetime default null
    )
    """
    DB.execute(query)
    
    query = """
    create table if not exists preferences (
      key text primary key, 
      value text not null
    )
    """
    DB.execute(query)
    
    try:
      DB.execute("insert into preferences values ('height', '300')")
      DB.execute("insert into preferences values ('width', '200')")
    except:
      LOG.info('Size preferences already exist...')
      
    try:
      DB.execute("insert into preferences values ('top', '0')")
      DB.execute("insert into preferences values ('left', '0')")
    except:
      LOG.info('Position preferences already exist...')
      
    try:
      DB.execute("insert into preferences values ('show_completed', 'False')")
    except:
      LOG.info('Task display preferences already exist...')
  
  def __get_preference(self, key):
    query = "select value from preferences where key = '%s' limit 1" % key
    # print query
    value = DB.execute(query).fetchone()[0]
    # print value
    return value

  def __set_preference(self, key, value):
    query = "update preferences set value = '%s' where key = '%s'" % (value, key)
    # print query
    return DB.execute(query)
  
  def __get_size_and_pos(self):
    height = int(self.__get_preference('height'))
    width = int(self.__get_preference('width'))
    top = int(self.__get_preference('top'))
    left = int(self.__get_preference('left'))
    return height, width, top, left
  
  def __save_settings(self):
    LOG.info('Saving application settings')
    width, height = self.window.get_size()
    self.__set_preference('height', height)
    self.__set_preference('width', width)
    
    left, top = self.window.get_position()
    self.__set_preference('top', top)
    self.__set_preference('left', left)
    
    DB.commit()
    DB.close()
  
  def add_task(self, widget, event, data=None):
    LOG.info('adding task')
  
  def edit_task(self, widget, event, data=None):
    LOG.info('editing task')
    
  def delete_task(self, widget, event, data=None):
    LOG.info('deleting task')
    
  def save_show_completed(self, widget, event, data=None):
    LOG.info('setting show completed to %s' % self.show_completed_button.get_active())
    self.__set_preference('show_completed', self.show_completed_button.get_active())
    
  def destroy(self, widget, event=None, data=None):
    self.__save_settings()
    gtk.main_quit()
    return False

def main():
  gtk.main()
  return 0
  
if __name__ == '__main__':
  pyTodo = PyTodo()
  main()