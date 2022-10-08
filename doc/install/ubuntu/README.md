# Documentation for Ubuntu
## Requirements
* Ubuntu 20.04
* PostgreSQL
* Git
* Python 3.8

## Installation
### Configure UTC
```commandline
sudo dpkg-reconfigure tzdata
```
### [PostgreSQL](./POSTGRESQL.md)
### [Dependencies](./DEPENDENCIES.md)
### Run (First activate python virtual environment)
* Check version
```
odoo --version
```
* Create database

Use this command only in first time for create the database, the parameters are:
  * -d [database name]
  * -r [username]
  * -w [password]
```
odoo -d odoo15 -r odoo15 -w o --stop-after-init
```
To initialize a database without demonstration data, add the **--without-demo=all** option to the odoo command.
### Configuring the Odoo server options
* To see all the available options
```
odoo --help
```
* Creates a new **odoo.conf** configuration file
```
odoo -c odoo.conf --save --stop
```
* Edit **odoo.conf**
  * db_name = odoo15
  * db_password = o
  * db_user = odoo15
### Run odoo server
```
odoo -c odoo.conf
```
### Access to server default URL
* HTTP service (werkzeug) running on http://localhost:8069
* Default username and password is: admin admin