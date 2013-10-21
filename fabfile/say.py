from fabric.api import env, hide, settings
import sys

def say(message=0):
    """internal command for message broadcast"""
    with settings( hide( 'everything' ), warn_only=True ):
        if message != 0:
            print ( '[%s] %s' % ( env['host'], message ) )
        else:
            sys.exit( "Error: Something told me to talk, but I'm all out of words..." )
