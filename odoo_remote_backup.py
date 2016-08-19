# -*- coding:utf-8 -*-

import urllib2
import urllib
from threading import Thread
import sys
import os
import xmlrpclib
import argparse

def print_loading():
    sys.stdout.write('.')
    sys.stdout.flush()

def get_backup(url, port, database_name, master_password):
    try:
        version_number = get_server_version(url, port)
        if version_number == 9:
            data = urllib.urlencode({'name':database_name, 'master_pwd':master_password})
        else:
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
        

def restore_database(url, port, database_name, master_password, database_file_url):
    try:
        if not database_file_url: raise Exception('Provide the --database_file command line argument')
        version_number = get_server_version(url, port)
        if version_number == 9:
            data = urllib.urlencode({'name':database_name, 'master_pwd':master_password, 'backup_file':database_file_url, 'copy': True})
        elif version_number == 8:
            data = urllib.urlencode({'new_db': database_name, 'restore_pwd':master_password, 'db_file':open(database_file_url), 'mode':'copy'}, True)
        request = urllib2.Request(url + ':%s' % (port) + '/web/database/restore' , data=data)
        print 'Restoring database to:'
        print url, ':', port
        open_conn = urllib2.urlopen(request)
        open_conn.read()
    except Exception, e:
        print '\n'
        print 'Database restoration failure: '
        print '================'
        print e
    else:
        print '\n'
        print 'Database restored at ' + str(url) + ' under the name: ' + database_name    
        


def get_server_version(url, port):
    try:
        common = xmlrpclib.ServerProxy('{}/xmlrpc/common'.format(url + ':' + str(port)))
        version = common.version().get('server_version_info', False)
        print 'Server version:', version[0] if version else 'Could not get server version info.'
    except xmlrpclib.Fault, e:
        print 'Could not get version info'
        print e
    else:
        return version[0]

def main(operation, url, port, database_name, master_password, database_file_url=None):
    if 'http://' not in url: url = 'http://' + url
    if operation == 'backup':
        thread = Thread(target=get_backup, args=(url, port, database_name, master_password))
    elif operation == 'restore':
        thread = Thread(target=restore_database, args=(url, port, database_name, master_password, database_file_url))
    thread.start()
    import time
    while thread.is_alive():
        print_loading()
        time.sleep(1.0)
        
# TODO restore database
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--operation', required=True, choices=['backup', 'restore'], help="Choose whether you want to backup or restore a database. Type 'backup' for backing up a database or 'restore' to restore a database to a server")
    parser.add_argument('--server_url', required=True, help="The server's url")
    parser.add_argument('--server_port', required=True, help="The port that the Openerp/Odoo server is listening to")
    parser.add_argument('--database_name', required=True, help="When the operation is 'backup' this is the name of the database to backup, when the operation is 'restore' this will be the new database's name.")
    parser.add_argument('--database_file', required=False, help="This argument is only applied when the operation is 'restore'. Pass here the *absolute* path to the dataase backup file you want to restore.")
    parser.add_argument('--admin_password', required=True, help="The admin pass of the Odoo server.")
    args = parser.parse_args()
    main(args.operation, args.server_url, args.server_port, args.database_name, args.admin_password, args.database_file,)



# if __name__ == '__main__':
#     try:
#         main(url=sys.argv[1], port=sys.argv[2] , database_name=sys.argv[3], master_password=sys.argv[4])
#     except IndexError:
#         print "Usage: python odoo_remote_backup.py operation('backup'|'restore') server_url server_port database_name admin_password"
#         print "When you backup a database the 'database_name' parameter should be the database name of the remote database"
#         print "When you restore a database to a remote server the 'database_name' parameter should be a " 
#     except Exception, e:
#         print e
        






























