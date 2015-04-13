# Import other Python files
from netbackup import *
from puppet import *
from say import *
from sshkey import *
from yum import *

# Import host configuration
from hosts import *

# Set Fabric to use SSH configurations from .ssh/config
env.skip_bad_hosts = True
env.use_ssh_config = True
