from fabric.api import run, settings, sudo
from fabric.contrib.files import exists

from say import *

#def puppet_test():
#    """Run puppet agent with the test flag"""
#    with settings( warn_only=True ):
#        if exists ( '/var/lib/puppet/state/agent_catalog_run.lock' ):
#            say ( 'Puppet is currently running on background - sleeping 15 secs' )
#            local ( 'sleep 15' )
        #result = sudo ('puppet agent --test --noop')
#        result = run ('sudo puppet agent --test --noop')
#        if result.return_code == 0:
#            say ( 'Puppet run - No changes performed' )
#        elif result.return_code == 1:
#            say ( 'Puppet run - Error returned, but continuing this time...' )
#        elif result.return_code == 2:
#            say ( 'Puppet run - PLEASE CHECK THIS, SHOULD NOT HAVE RETURNED 2!!!' )
#        else:
#            sys.exit( 'Puppet command returned unexpected error %s' % ( result.return_code ) )

#def puppet_update():
#    """Run puppet agent, forcing system update"""
#    with settings( warn_only=True ):
#        if exists ( '/var/lib/puppet/state/agent_catalog_run.lock' ):
#            say ( 'Puppet is currently running on background - sleeping 20 secs' )
#            local ( 'sleep 20' )
#        result = run ('sudo /usr/bin/puppet agent --test --no-noop')
        # Alternative if hosts have not been set up with suoders access
        # result = sudo ('puppet agent --test --no-noop')
#        if result.return_code == 0:
#            say ( 'Puppet run - No changes performed' )
#        elif result.return_code == 2:
#            say ( 'Puppet run - System has been updated' )
#        else:
#            sys.exit( 'Puppet command returned unexpected error %s' % ( result.return_code ) )

def puppet_test(tags='', extra_args='', **kwargs):
    """Call puppet to run on test mode"""
    result = puppet_run(True, tags, extra_args)

def puppet_update(tags='', extra_args='', **kwargs):
    """Call puppet to run on update mode"""
    result = puppet_run(False, tags, extra_args)

def puppet_run(is_noop=True, tags='', extra_args=''):
    """Run puppet agent on remote host"""
    noop_arg = "--noop" if is_noop else "--no-noop"
    tags_arg = ("--tags %s" % tags) if tags else ""
    puppet_command = "sudo /usr/bin/puppet agent --test %s %s %s" % (noop_arg, tags_arg, extra_args)

    with settings( warn_only=True ):
        if exists ( '/var/lib/puppet/state/agent_catalog_run.lock' ):
            say ( 'Puppet is currently running on background - sleeping 10 secs' )
            local ( 'sleep 10' )
        result = run ( puppet_command )
        if result.return_code == 0:
            say ( 'Puppet run - No changes performed' )
        elif result.return_code == 1:
            say ( 'Puppet run - Error returned, but continuing this time...' )
        elif result.return_code == 2:
            if is_noop:
                say ( 'Puppet run - PLEASE CHECK THIS, SHOULD NOT HAVE RETURNED 2!!!' )
            else:
                say ( 'Puppet run - System has been updated' )
        else:
            sys.exit( 'Puppet command returned unexpected error %s' % ( result.return_code ) )

def puppet_kill():
    """Kill all puppet instances, beware running this on the puppetmaster"""
    with settings( warn_only=True ):
        sudo ( '/usr/bin/killall puppet')
