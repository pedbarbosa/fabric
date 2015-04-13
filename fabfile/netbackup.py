from fabric.api import run, env, sudo, settings, hide, parallel, put
from termcolor import colored

import re, os, sys

def netbackup(auto='no'):
	"""Checks NetBackup settings and updates server list and exclusions"""
	# TODO - application still brakes if one of the host is unreachable
	# TODO - server list only applies to PROD, get list for other environments
	with settings( hide( 'everything' ), warn_only=True ):
		error = False
		
		# List of exclusions to be added to exclude_list
		netbackup_exclusions = ['/dev', '/proc', '/sys', '/tmp', '/u0*', '/usr/openv', '/var/cache', '/var/lib/mysql', '/var/lock', '/var/run', '/var/spool/postfix', '/var/tmp', '/var/www/cache', 'thread-dump*']
		
		# NetBackup folder
		nb_path = '/usr/openv/netbackup/'
		# Status output
		print ( 'Checking %s... ' % env['host'] ),

		# Get hostname and RHEL version
		hostname = run( 'hostname' )
		os_version = re.search( '\s\d.*', run( 'cat /etc/redhat-release' ) )
		# Output host info
		print ( '\r[%s RHEL%s]' % ( env['host'], os_version.group(0) ) ),

		# Check if NetBackup conf is present
		exists = run( 'cat %sbp.conf' % nb_path )
		if not exists.succeeded:
			# Return NetBackup not found
			print colored( 'NetBackup is not installed or configured properly!', 'red' )
		else:
			# Get details on NetBackup
			try: nb_servers = int ( run ('grep SERVER %s/bp.conf | wc -l' % nb_path ) )
			except: nb_servers = 0
			try: nb_exclusions = int ( run ('cat %s/exclude_list | wc -l' % nb_path ) )
			except: nb_exclusions = 0
			nb_version = re.search( '\s\d.*', run( 'cat %sbin/version' % nb_path ) )
						
			# Output NetBackup version
			print ( 'NetBackup%s:' % nb_version.group(0) ),
			
			# Check hostname in bp.conf
			match = re.search( '(\S+)$', run( 'grep CLIENT_NAME %s/bp.conf' % nb_path ) )
			if match:
				if match.group(1).strip().lower() != hostname.strip().lower():
					error = True
					print colored( 'bp.conf error -> CLIENT = %s HOSTNAME = %s!' % ( match.group(1), hostname ), 'magenta' )
			else:
				# Capture unexpected exceptions
				error = True

			# Check for number of servers
			if nb_servers != 4:
				error = True
				print colored( 'Configured incorrectly with %s servers!' % nb_servers, 'yellow' )
			
			# Check for entries in the exception list
			if nb_exclusions != len(netbackup_exclusions):
				error = True
				print colored( 'Exclusion file has %s exclusions instead of %s!' % ( nb_exclusions, len(netbackup_exclusions) ), 'cyan' )
				
			# Determine if NetBackup configuration needs update
			if error == True:
				fix = 'x'
				# To automate this process use 'netbackup:auto=yes' on the command line
				if auto != 'yes':
					# Prompt user for fix
					while fix != 'Y'.lower() and fix != 'N'.lower():
						fix = raw_input( 'Shall I refresh bp.conf and exclusion_list, and restart NetBackup (y/n)? ' )

				if auto == 'yes' or fix == 'y':
					# Create files on /tmp
					run ( "echo 'SERVER = wtfmilnbu1.core.wotifgroup.com\nSERVER = syd2nbu1.prod.wotifgroup.com\nSERVER = bne2nbu1.prod.wotifgroup.com\nSERVER = wgsyd2nba1.core.wotifgroup.com\nCLIENT_NAME =' $HOSTNAME > /tmp/bp.conf" )
					run ( "echo '" + '\n'.join([`excl` for excl in netbackup_exclusions]).replace("'", "") + "' > /tmp/exclude_list" )
					# Copy files from tmp to NetBackup directory and restart NetBackup
					sudo ( 'sudo cp /tmp/bp.conf /tmp/exclude_list %s/; sudo /etc/init.d/netbackup stop; sudo /etc/init.d/netbackup start' % nb_path )
					print ( '\r[%s RHEL%s] NetBackup%s reconfigured and restarted' % ( env['host'], os_version.group(0), nb_version.group(0) ) )
			else:
				print colored( 'Configured correctly with %s servers and %s exclusions!' % ( nb_servers, nb_exclusions ), 'white' )

def netbackup_rhel75():
    with settings( hide( 'everything' ), warn_only=True ):
        sudo ( 'rm /usr/openv/netbackup/exclude_list.PROD_syd2_RHEL' )
        sudo ( 'ln -s /usr/openv/netbackup/exclude_list /usr/openv/netbackup/exclude_list.PROD_syd2_RHEL' )
