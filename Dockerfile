FROM python:latest
MAINTAINER eavictor
COPY . /home
WORKDIR /home
RUN apt-get update &&\
# install package configure utility
apt-get install -y apt-utils &&\
apt-get upgrade -y &&\

# install mariadb repository
apt-get install -y software-properties-common &&\
apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 0xcbcb082a1bb943db &&\
#add-apt-repository 'deb [arch=amd64,i386] http://mirrors.accretive-networks.net/mariadb/repo/10.1/debian jessie main' &&\
echo '# MariaDB 10.1 repository list - created 2016-09-25 15:29 UTC' >> /etc/apt/sources.list &&\
echo '# http://downloads.mariadb.org/mariadb/repositories/' >> /etc/apt/sources.list &&\
echo 'deb [arch=amd64,i386] http://mirrors.accretive-networks.net/mariadb/repo/10.1/debian jessie main' >> /etc/apt/sources.list &&\
echo 'deb-src http://mirrors.accretive-networks.net/mariadb/repo/10.1/debian jessie main' >> /etc/apt/sources.list &&\

# install mariadb
apt-get update &&\
echo 'mariadb-server-10.1 mysql-server/root_password password Passw0rd' >> debconf-set-selections &&\
echo 'mariadb-server-10.1 mysql-server/root_password_again passowrd Passw0rd' >> debconf-set-selections &&\
DEBIAN_FRONTEND=noninteractive apt-get install -y mariadb-server

# configure mariadb
RUN service mysql stop
RUN cp /home/server_settings/my.cnf /etc/mysql/my.cnf
RUN service mysql start &&\
mysql -uroot -pPassw0rd -e 'SET @@GLOBAL.wait_timeout = 600; SET @@SESSION.wait_timeout = 600; SET @@LOCAL.wait_timeout = 600; CREATE DATABASE geoip; CREATE DATABASE ads; COMMIT; EXIT' &&\
systemctl enable mariadb.service #TODO: register MariaDB(mysql) as system service (start when docker up)