from fabric.api import run, settings, sudo
from fabric.contrib.files import exists

from say import *

def puppet_test():
    """Run puppet agent with the test flag"""
    with settings( warn_only=True ):
        if exists ( '/var/lib/puppet/state/agent_catalog_run.lock' ):
            say ( 'Puppet is currently running on background - sleeping 15 secs' )
            local ( 'sleep 15' )
        result = sudo ('puppet agent --test --noop')
        if result.return_code == 0:
            say ( 'Puppet run - No changes performed' )
        elif result.return_code == 1:
            say ( 'Puppet run - Error returned, but continuing this time...' )
        elif result.return_code == 2:
            say ( 'Puppet run - PLEASE CHECK THIS, SHOULD NOT HAVE RETURNED 2!!!' )
        else:
            sys.exit( 'Puppet command returned unexpected error %s' % ( result.return_code ) )

def puppet_update():
    """Run puppet agent, forcing system update"""
    with settings( warn_only=True ):
        if exists ( '/var/lib/puppet/state/agent_catalog_run.lock' ):
            say ( 'Puppet is currently running on background - sleeping 15 secs' )
            local ( 'sleep 20' )
        # Replace once all hosts have been set up with sudoers access
        # result = run ('sudo puppet agent --test --no-noop')
        result = sudo ('puppet agent --test --no-noop')
        if result.return_code == 0:
            say ( 'Puppet run - No changes performed' )
        elif result.return_code == 2:
            say ( 'Puppet run - System has been updated' )
        else:
            sys.exit( 'Puppet command returned unexpected error %s' % ( result.return_code ) )

def puppet_kill():
    """Kill all puppet instances, beware running this on the puppetmaster"""
    with settings( warn_only=True ):
        sudo ( '/usr/bin/killall puppet')
