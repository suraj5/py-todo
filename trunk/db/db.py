import logging
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
  
  def save_settings(self):
    LOG.info('Saving application settings')
    
    __DB__.commit()
    __DB__.close()
