# Docker patchman
This is a dockerized version which checks out the latest from patchman master. It has a modified host package list, to enable viewing solely security updates.

## Test instance
A docker-compose is included to allow you to start testing right away. You will need to exec
into the mysql container and run the commands in the next step manually on first run.

## MySQL db config
The following MySQL commands should be modified and run prior to starting up your container.
```
mysql> CREATE DATABASE patchman CHARACTER SET utf8 COLLATE utf8_general_ci;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON patchman.* TO patchman@'%' IDENTIFIED BY 'coolpw';
Query OK, 0 rows affected (0.00 sec)
```

## Environment varibales
- ADMINNAME: Administrator full name (Don't include a space; May break.)
- ADMINEMAIL: Administrator email address
- ADMINACC: Administrator username
- ADMINPW= Administrator password
- DBNAME: Name of MySQL database
- DBUSER: Username for MySQL
- DBPW: MySQL password
- DBHOST: MySQL server address
- SECRETKEY: Patchman's secret key (set what you want)

## Credits
You can find patchman over at [the patchman github repo.](https://github.com/furlongm/patchman)
