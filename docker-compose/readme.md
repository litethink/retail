login
mysql -u root -p
//查看用户的远程登录权限
use mysql
select host,user from user;


show databases;






#
docker exec -it $container sh 

//for show all content of command.
docker ps --no-trunc



并行运行
command:
    - sh
    - -c 
    - |
        cmd1 &
        cmd2 &
        cmd3
