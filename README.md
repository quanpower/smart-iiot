Smart-iiot
======
smart-iiot based on flask & react.

python3.5

Using:Flask Blueprint,Flask-migrate,Flask-SQLAlchemy,Flask-Login,Flask-Mail,Flask-WTF,Flask-Bootstrap,flask-cli(click),


1.Set .env
--------------------------------------------

Config:key-value

2.Update database
--------------------------------------------

Flask deploy 
or
flask db upgrade

3.Run
--------------------------------------------

export FLASK_APP=smart-iiot.py
flask run

4.Gunicorn
--------------------------------------------

exec gunicorn -b :5000 --access-logfile - --error-logfile - smart-iiot:app

5.Boot
--------------------------------------------

./boot.sh


6.Aliyun deploy
---------------------

1>ssh root@120.78.70.211
2>apt-get update && apt-get upgrade
3>apt-get install python3-dev
3>apt-get install git
4>pip install virtualenv
5>git clone https://github.com/quanpower/smart-iiot.git
6>cd smart-iiot && virtualenv venv --python=python3
7>source venv/bin/activate
8>pip install -r requirements.txt
9>apt-get install nginx
10>cp ~/smart-iiot/antd-nginx.conf /etc/nginx/conf.d
11>flask migrate && flask deploy
12>exec gunicorn -b :5000 --access-logfile - --error-logfile - smart-iiot:app
13>supervisord
# 生成默认配置文件  
echo_supervisord_conf > /etc/supervisord.conf  

mkdir -m 755 -p /etc/supervisor/
mkdir -m 755 conf.d
echo_supervisord_conf > /etc/supervisor/supervisord.conf 

include区段修改为：  
[include]  
files = /etc/supervisor/conf.d/*.conf
mv smart-iiot.conf /etc/supervisor/conf.d
如需要访问web控制界面，inet_http_server区段修改为：  
[inet_http_server]  
port=0.0.0.0:9001  
username=username ; 你的用户名  
password=password ; 你的密码
每个需要管理的进程分别写在一个文件里面，放在/etc/supervisord.conf.d/目录下，便于管理。例如：test.conf  
[program:sqlparse]  
directory = /var/www/python  
command = /bin/env python test.py

supervisord -c /etc/supervisor/supervisord.conf
