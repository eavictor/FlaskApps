# FlaskApps
### GeoIP list for routers with
### Ad Servers list for routers

Feature list:

 * RESTful Server API compatible for all Routers
 * Built in MikroTik RouterOS support

## API Reference
There are 2 ways to get API Reference

 * http://www.eavictor.com/
 * After Server is up and running

## Installation

#### Ubuntu Server 16.04

01.reconfigure timezone, just hit enter because this project needs UTC timezone
```
sudo dpkg-reconfigure tzdata
```

02.[install and configure MariaDB](https://eavictor.wordpress.com/2016/05/04/install-mariadb-10-1-on-ubuntu-server-16-04-lts-access-from-remote-client/) or other SQLAlchemy supported Databases.

03.install required pacakages, if you don't use MariaDB or MySQL, then you don't have to install libmysqlclient-dev
```
sudo apt-get install -y python3 python3-pip python3-dev libmysqlclient-dev nginx
```

04.upgrade python3-pip
```
sudo python3 -m pip install --upgrade pip
```

05.install python3 virtualenv
```
sudo pip3 install virtualenv
```

06.create project Folder under /home/{username}
```
mkdir FlaskApps
cd FlaskApps
```

07.create python3 virtualenv and activate the virtualenv just created. you will see (venv) on your command prompt
```
python3 -m virtualenv venv
source venv/bin/activate
```

08.check virtualenv version. It should be 3.5.1 or newer.
```
python -V
```

09.install python3 packages and uwsgi. If you don't use MariaDB or MySQL, don't install mysqlclient
```
pip install flask flask-sqlalchemy apscheduler mysqlclient uwsgi
```

10.deactivate virtualenv
```
deactivate
```

11.create systemd unit file
```
sudo nano /etc/systemd/system/FlaskApps.service

copy, replace {username} with your username and paste:
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[Unit]
Description=uWSGI instance to serve FlaskApps
After=network.target

[Service]
User={username}
Group=www-data
WorkingDirectory=/home/{username}/FlaskApps
Environment="PATH=/home/{username}/FlaskApps/venv/bin"
ExecStart=/home/{username}/FlaskApps/venv/bin/uwsgi --ini FlaskApps.ini

[Install]
WantedBy=multi-user.target
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```

12.enable FlaskApps
```
sudo systemctl start FlaskApps
sudo systemctl enable FlaskApps
```

13.configure nginx to proxy requests, server name should equals to you the domain name you put in browser or you'll get 404 not found error
```
sudo nano /etc/nginx/sites-available/FlaskApps

copy, replace {username} and {domain/IP} with your username, domain/IP and paste:
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
server {
	listen 80;
	server_name {domain/IP};
	
	location / {
		include uwsgi_params;
		uwsgi_pass unix:/home/{username}/FlaskApps/FlaskApps.sock;
	}
}
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

```

14.enable nginx server block
```
sudo ln -s /etc/nginx/sites-available/FlaskApps /etc/nginx/sites-enabled
```

15.check nginx syntex
```
sudo nginx -t
```

16.restart nginx
```
sudo systemctl restart nginx
```

17.configure firewall
```
sudo ufw allow 'Nginx Full'
```