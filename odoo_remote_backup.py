# -*- coding:utf-8 -*-

import sys
import urllib2
import urllib

def get_database_backup(url, port, database_name, master_password):
    if 'http://' not in url: url = 'http://' + url
    data = urllib.urlencode({'backup_db':database_name, 'backup_pwd':master_password, 'token': None}, True)
    request = urllib2.Request(url + ':%s' % (port) + '/web/database/backup' , data=data)
    print 'Getting backup from:'
    print url
    open_conn = urllib2.urlopen(request)
    response = open_conn.read()
    _file = open(database_name, 'w')
    _file.write(response)
    _file.close()

if __name__ == '__main__':
    try:
        get_database_backup(url=sys.argv[1], port=sys.argv[2] , database_name=sys.argv[3], master_password=sys.argv[4])
    except IndexError:
        print '\n\n\nUsage: python odoo_remote_backup server_url server_port database_name admin_password'
    except Exception, e:
        print e
        



