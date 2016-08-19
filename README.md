## Works for openerp v7, odoo v8, odoo v9


Run the following command

```python odoo_remote_backup server_url server_port database_name admin_password```

*Note*: All arguments are required.

Running the above command will fetch a database backup to your local machine that will be saved in the same directory as this script.

*Note 2*: Unfortunately, if a database does not exist there, is no way to report this from within the script because the "Database does not exist" error 
 that is thrown on the server is not being sent as a response to the client. The same thing will happen with some other errors that are not reported to the client
 So if you have trouble restoring the database, check the server logs for any issues there.