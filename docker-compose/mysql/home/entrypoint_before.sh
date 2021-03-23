#!/bin/sh
#No need change for any required this container.But need write or change commond to init.sql

if [ ! -d "/var/lib/mysql/$MYSQL_DATABASE" ];then                                                                                                                                                                                  
    echo "Initializing container" 
    
    cp /home/init.sql /docker-entrypoint-initdb.d                        
                                                                                                                                                        
fi                                                                                     

exec docker-entrypoint.sh mysqld
