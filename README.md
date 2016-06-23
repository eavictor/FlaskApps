# FlaskApps
### contain apps:
### 1. ads: Ad Servers list for routers
### 2. conoha: ConoHa API for download and mount custom ISO
### 3. geoip: GeoIP list for routers
### 4. root: index page

Feature list:

 * RESTful Server API compatible for all Routers
 * Built in MikroTik RouterOS support

## API Reference
There are 2 ways to get API Reference

 * http://www.eavictor.com/
 * After Server is up and running

## Installation

#### Ubuntu Server 16.04

00.upgrade ubuntu system packages
```
sudo apt-get update && apt-get upgrade -y
```
if your server doesn't contains any other things or you just don't care this command may harm your server, you can also execute
```
sudo apt-get dist-upgrade
```

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

06.create project Folder under /home/[username]
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
pip install flask flask-sqlalchemy apscheduler mysqlclient requests uwsgi
```

10.deactivate virtualenv, change to use home dictionary, clone the project and modify SQL settings
```
deactivate
cd /home/[username]
git clone https://github.com/eavictor/FlaskApps
cd ./FlaskApps
sudo nano settings.py
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
```
choose one of setting template below, replace [username] and [domain and/or IP] with your username, domain and/or IP and copy paste:
```
# http only
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
server {
	listen 80;
	server_name [domain and/or IP];
	
	location / {
		include uwsgi_params;
		uwsgi_pass unix:/home/[username]/FlaskApps/FlaskApps.sock;
	}
}
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# http with client IP address in header(so we can get client's IP address through nginx proxy)
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
server {
	listen 80;
	server_name [domain and/or IP];
	
	location / {
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
		proxy_set_header host $host;
		include uwsgi_params;
		uwsgi_pass unix:/home/[username]/FlaskApps/FlaskApps.sock;
	}
}
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```
if you need https feature, please upload your certificate (including certificate chain) to /home/[username]/SSL and execute extra commands

Warning: certificate order matters !! also do not put root CA into this command !!
```
sudo cat /home/[username]/SSL/[your public crt name].crt /home/[username]/SSL/[domain validation crt name].crt /home/[username]/SSL/[add trust ca crt name].crt > /home/[username]/SSL/[your public crt name].certchain.crt
sudo chmod -c 400 STAR_eavictor_com.certchain.crt
sudo chmod -c 400 STAR_eavictor.com.key
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
```
then choose one of setting template below, replace [username] and [domain and/or IP] with your username, domain and/or IP and copy paste:
```
# http and https (without auto-redirect to https)
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
server {
	listen 80;
	server_name [domain and/or IP];
	
	location / {
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
		proxy_set_header host $host;
		include uwsgi_params;
		uwsgi_pass unix:/home/[username]/FlaskApps/FlaskApps.sock;
	}
}
server {
	listen 443 http2;
	ssl on;
	server_name [domain and/or IP];
	
	# SSL certificate
	ssl_certificate /home/[username]/SSL/[your public crt name].certchain.crt;
	ssl_certificate_key /home/[username]/[your private key name].key;
	
	# Connection credentials caching
	ssl_session_cache shared:SSL:20m;
	ssl_session_timeout 60m;
	
	# Disable old SSL
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
	
	# Optimize cipher suites
	ssl_ciphers "ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5";
	ssl_prefer_server_ciphers on;
	ssl_dhparam /etc/ssl/certs/dhparam.pem;
	
	ssl_session_tickets off;
	ssl_stapling on;
	ssl_stapling_verify on;
	resolver 8.8.8.8 8.8.4.4 valid=300s;
	resolver_timeout 5s;
	
	add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
	add_header X-Frame-Options DENY;
	add_header X-Content-Type-Options nosniff;
	
	location / {
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
		proxy_set_header host $host;
		include uwsgi_params;
		uwsgi_pass unix:/home/[username]/FlaskApps/FlaskApps.sock;
    }
}
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#http and https(with auto-redirect to https)
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
server {
	listen 80;
	server_name [domain and/or IP];
	return 301 https://$server_name$request_uri;
}
server {
	listen 443 ssl http2;
	server_name [domain and/or IP];
	
	# SSL certificate
	ssl_certificate /home/[username]/SSL/[your public crt name].certchain.crt;
	ssl_certificate_key /home/[username]/SSL/[your private key name].key;
	
	# Connection credentials caching
	ssl_session_cache shared:SSL:20m;
	ssl_session_timeout 60m;
	
	# Disable old SSL
	ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
	
	# Optimize cipher suites
	ssl_ciphers "ECDH+AESGCM:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5";
	ssl_prefer_server_ciphers on;
	ssl_dhparam /etc/ssl/certs/dhparam.pem;
	
	ssl_session_tickets off;
	ssl_stapling on;
	ssl_stapling_verify on;
	resolver 8.8.8.8 8.8.4.4 valid=300s;
	resolver_timeout 5s;
	
	add_header Strict-Transport-Security "max-age=63072000; includeSubdomains; preload";
	add_header X-Frame-Options DENY;
	add_header X-Content-Type-Options nosniff;
	
	location / {
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header x-forwarded-for $proxy_add_x_forwarded_for;
		# proxy_set_header host $host;
		include uwsgi_params;
		uwsgi_pass unix:/home/[username]/FlaskApps/FlaskApps.sock;
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

18.upgrade all ubuntu python packages(maintenance only)
```
sudo apt-get update && apt-get upgrade -y
source /home/[username]/FlaskApps/venv/bin/activate
python -m pip install --upgrade pip
pip install --upgrade flask flask-sqlalchemy apscheduler mysqlclient requests uwsgi
deactivate
```