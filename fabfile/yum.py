from fabric.api import sudo

def yumcleanall():
    """cleans up yum cache"""
    sudo ( 'yum clean all' )
