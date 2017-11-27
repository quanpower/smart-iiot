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