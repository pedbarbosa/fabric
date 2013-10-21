# Import other Python files
from puppet import *
from say import *
from sshkey import *
from yum import *

# Set Fabric to use SSH configurations from .ssh/config
env.use_ssh_config = True
