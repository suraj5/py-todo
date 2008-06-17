import metakit
import os

print 'Using MetaKit %s' % metakit.version

# determine where the user's home directory is
USER_HOME = os.path.expanduser('~')
USER_PREF = os.path.join(USER_HOME, '.pytodo')

if not os.path.exists(USER_PREF):
    # create the preferences directory if it doesn't exist
    os.mkdir(USER_PREF)

class DBA:
    _db = metakit.storage(os.path.join(USER_PREF, 'tasks.mk'), 1)
    
    def __init__(self):
        pass
    
    def save_task(self, task):
        pass

class Task(object):
    def __init__(self, id=0, task=None, priority=None, tags=None, due_by=None,
                 description=None, completed=None):
        self.id = id
        self.task = task
        self.priority = priority
        self.tags = tags
        self.due_by = due_by
        self.description = description
        self.completed = completed
