#!/bin/bash
# Проверка, что мы рутовый пользователь
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ -f "/etc/debian_version" ]; then
   # do stuff
fi

if [ -f "/etc/debian_version" ]
then
  echo "Linux is Ok"
else
    echo "This bash script is only for debian"
    return 1 2>/dev/null
    exit 1
fi

# Обновление системы
apt-get update
apt-get upgrade

#Установка необходимых пакетов
apt-get -y install python3 python3-pip curl mariadb-server

echo "Updating mysql configs in /etc/mysql/my.cnf."

if [ 'sed -i "s/.*bind-address.*/bind-address = 192.168.100.160/" /etc/mysql/mariadb.conf.d/50-server.cnf' ]; then

    echo "Updated mysql bind address in /etc/mysql/my.cnf to 0.0.0.0 to allow external connections."

    /etc/init.d/mysql stop
    /etc/init.d/mysql start

fi

#Создание БД
#mysql  -u root -e "CREATE USER 'Solidworks'@'localhost' IDENTIFIED BY 'Пароль от бд';"
#mysql  -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'Имя пользователя бд'@'localhost';"
mysql  -u root -e "CREATE USER 'Имя пользователя бд'@'%' IDENTIFIED BY 'Пароль от бд';"
mysql  -u root -e "GRANT ALL PRIVILEGES ON *.* TO 'Имя пользователя бд'@'%';"
# Make our changes take effect
mysql -e "FLUSH PRIVILEGES"

#Для соединения использовать:
#mysql -u 'Имя пользователя бд' -p'Пароль от бд' -h pmelikov.ru -P 46306


# Обновление pip3
#python3 -m pip3 –version
pip3 install --upgrade pip setuptools wheel
pip3 install Flask flask_sqlalchemy flask-cors

# Установка nodejs
curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
apt-get install -y nodejs


mkdir /hackinhome2021
cd /hackinhome2021
