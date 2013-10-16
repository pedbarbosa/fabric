# Import Fabric functions
from fabric.api import env, run, settings, hide

# Import Fabric modules
import os, sys

def sshkey():
    """Pushes personal SSH key for server authentication"""
    with settings( hide( 'everything' ), warn_only=True ):
        print ( '\rChecking %s... ' % env['host'] ),

        try:
            dsa = open( os.getenv('HOME') + '/.ssh/id_dsa.pub', 'r' ).readline().split()
        except IOError as e:
            sys.exit( 'SSH ID file not found' )
        run( 'if [ -d .ssh ]; then true; else mkdir .ssh; fi' )
        exists = run( 'grep \'%s\' ~/.ssh/authorized_keys' % dsa[1] )
        if not exists.succeeded:
            run ( 'echo %s %s %s >> ~/.ssh/authorized_keys' % (dsa[0], dsa[1], dsa[2]) )
            print 'SSH key added!'
        else:
            print 'SSH key already present, no update required'
