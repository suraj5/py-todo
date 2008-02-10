import logging#, dateutil
from datetime import datetime
from pysqlite2 import dbapi2 as sqlite

# connect to the database
__DB__ = sqlite.connect('pytodo.db')

# setup the logger
level = logging.DEBUG
f = '%(asctime)s: %(levelname)s; %(name)s (%(lineno)d) %(message)s'

LOG = logging.getLogger('Database')
LOG.setLevel(level)

ch = logging.StreamHandler()
ch.setLevel(level)

formatter = logging.Formatter(f)
ch.setFormatter(formatter)
LOG.addHandler(ch)

# 2008-02-08 22:52:40.437000
#FORMAT = '%Y-%m-%d %H:%M:%S'
FORMAT = '%c'

class Task:
  def __init__(self, *kargs, **kwargs):
    self.id = kwargs['id']
    self.parent = kwargs['parent']
    self.description = kwargs['description']
    
    if kwargs['complete'] == 0:
      self.complete = False
    else:
      self.complete = True
    
    self.date_created = kwargs['date_added']#, FORMAT)
    self.date_due = kwargs['date_due']#, FORMAT)
    
    self.children = []

class Database:
  def check_tables(self):
    """Make sure that the appropriate tables exist in the database, along with
    some default settings."""
    
    # create the tasks table
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
    __DB__.execute(query)
    
    # create the preferences table
    query = """
    create table if not exists preferences (
      key text primary key, 
      value text not null
    )
    """
    __DB__.execute(query)
    
    # save size preferences
    try:
      __DB__.execute("insert into preferences values ('height', '300')")
      __DB__.execute("insert into preferences values ('width', '200')")
    except:
      LOG.info('Size preferences already exist...')
      
    # save position preferences
    try:
      __DB__.execute("insert into preferences values ('top', '0')")
      __DB__.execute("insert into preferences values ('left', '0')")
    except:
      LOG.info('Position preferences already exist...')
    
    # save task display preferences
    try:
      __DB__.execute("insert into preferences values ('show_completed', 'False')")
    except:
      LOG.info('Task display preferences already exist...')
  
  def get_setting(self, key):
    query = "select value from preferences where key = '%s' limit 1" % key
    value = __DB__.execute(query).fetchone()[0]
    return value

  def set_setting(self, key, value):
    query = "update preferences set value = '%s' where key = '%s'" % (value, key)
    return __DB__.execute(query)
  
  def get_size_and_pos(self):
    height = int(self.get_setting('height'))
    width = int(self.get_setting('width'))
    top = int(self.get_setting('top'))
    left = int(self.get_setting('left'))
    return height, width, top, left
    
  def get_all_tasks(self):
    return self.__get_tasks_by_parent(None)
    
  def __get_tasks_by_parent(self, parent):
    #LOG.info('Retrieving children for parent: %s' % parent)
    tasks = []
    
    if parent == None or parent.id == None:
      p = 'is null'
    else:
      p = '= %d' % parent.id
      
    results = __DB__.execute('select * from tasks where parent_id %s order by date_due' % p)
    for (id, parent_id, description, complete, date_added, date_due) in results:
      t = Task(id=id, 
               parent=parent_id, 
               description=description, 
               complete=complete, 
               date_added=date_added, 
               date_due=date_due)
      
      t.children = self.__get_tasks_by_parent(t)
      tasks.append(t)
      
    return tasks
    
  def add_task(self):
    LOG.info('adding a task to the db')
    __DB__.execute("insert into tasks (description, complete, date_due) values ('', 0, '%s')" % datetime.now())
    return __DB__.execute('select last_insert_rowid()').fetchone()[0]
    
  def edit_task(self, task):
    LOG.info('editing task %i' % task[0])
    for a in task:
      print a, type(a)
    
    if task[3] == True:
      complete = True
    else:
      complete = False
    
    query = "update tasks set complete=%i, description='%s', date_due='%s' where id=%i" % (complete,
                                                                                           task[1].replace('\'','`'),
                                                                                           task[2].replace('\'','`'),
                                                                                           task[0])
    print query
    __DB__.execute(query)
  
  def save_settings(self):
    LOG.info('Saving application settings')
    
    __DB__.commit()
    __DB__.close()
