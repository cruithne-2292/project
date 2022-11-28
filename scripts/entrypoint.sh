#!/bin/bash

# start database daemon
service mariadb start

# create database credentials
mysql -u root -proot -e "
USE mysql;
ALTER USER 'root'@'localhost' IDENTIFIED BY 'root';  
FLUSH PRIVILEGES;
"
# create database
mysql -u root -proot -e "CREATE DATABASE project;"
# migrate database
python manage.py migrate
# create super user
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('manager', '', '12345678')" | python manage.py shell

# start gunicorn
exec gunicorn project.wsgi:application \
	--bind 0.0.0.0:8080 \
	--workers 1 \
	--timeout 240 \
	--access-logfile /var/log/gunicorn/access.log \
	--error-logfile /var/log/gunicorn/error.log >> /var/log/gunicorn/output.log 2>&1
