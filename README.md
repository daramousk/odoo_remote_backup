## Works for openerp v7, odoo v8, odoo v9
## On version 9 there was a bug that prohibited the backing up of a database. This has been resolved in https://github.com/odoo/odoo/issues/13192,
## make sure you update the server files up until that commit 54e4f3f96b0a93bbdee5cdffd6f671b812644a67

Run the following command

```python odoo_remote_backup --operation {backup,restore} --server_url --server_port --database_name --admin_password --database_file```

--database_file is the *absolute* url to the database zip file to restore. This argument is only used when the operation is restore

Run the script with the -h flag to get more info on the arguments.

Backup operation: Running the backup operation will fetch a database backup to your local machine that will be saved in the same directory as this script.

Restore operation: Running the restore operation will restore a database backup to a remote machine.

*Note*: Unfortunately, some errors that might occur on the server side such as database already exists, or wrong admin password do not get propagated back to the script and the script's operation might be falsely reported as successful. If you have any trouble restoring the database on a server later on, check the server logs for any errors.