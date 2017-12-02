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
