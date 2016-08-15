# -*- coding:utf-8 -*-

import urllib2
import urllib
from threading import Thread
import sys
import os
import xmlrpclib

def print_loading():
    sys.stdout.write('.')
    sys.stdout.flush()

def get_backup(url, port, database_name, master_password):
    try:
        print 'getbackup started'
        get_server_version(url, port)
        # TODO get database format (zip, dump, with filestore)
        data = urllib.urlencode({'backup_db':database_name, 'backup_pwd':master_password, 'token': None}, True)
        request = urllib2.Request(url + ':%s' % (port) + '/web/database/backup' , data=data)
        print 'Getting backup from:'
        print url, ':', port
        open_conn = urllib2.urlopen(request)
        response = open_conn.read()
        _file = open(database_name, 'w')
        _file.write(response)
        _file.close()
    except Exception, e:
        print '\n'
        print 'Backup failure: '
        print '================'
        print e
    else:
        print '\n'
        print 'Database backup completed.'
        print 'Database location', sys.path[0] + os.sep + database_name


def get_server_version(url, port):
    try:
        common = xmlrpclib.ServerProxy('{}/xmlrpc/common'.format(url + ':' + str(port)))
        version = common.version().get('server_version_info', False)
        print 'Server version:', version[0] if version else 'Could not get server version info.'
    except xmlrpclib.Fault, e:
        print 'Could not get version info'
        print e

def main(url, port, database_name, master_password):
    if 'http://' not in url: url = 'http://' + url
    # TODO find out if there is a way we can get the database size and show a percentage
    thread = Thread(target=get_backup, args=(url, port, database_name, master_password))
    thread.start()
    import time
    while thread.is_alive():
        print_loading()
        time.sleep(1.0)
        
# TODO make database_name optional, if not provided list all the databases that exist on the server
# TODO admin password should not be provided in the beginning for security reasons
if __name__ == '__main__':
    try:
        main(url=sys.argv[1], port=sys.argv[2] , database_name=sys.argv[3], master_password=sys.argv[4])
    except IndexError:
        print '\n\n\nUsage: python odoo_remote_backup server_url server_port database_name admin_password'
    except Exception, e:
        print e
        
