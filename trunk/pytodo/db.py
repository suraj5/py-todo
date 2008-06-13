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