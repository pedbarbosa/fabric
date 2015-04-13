from fabric.api import sudo

def yumcleanall():
    """cleans up yum cache"""
    sudo ( 'yum clean all' )

def rempdde():
    """Removes stupid NetBackup package"""
    sudo ( 'rpm -e --nodeps SYMCpddea' )
