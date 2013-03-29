# https://newrelic.com/docs/python/python-agent-and-tornado
web: gunicorn -k tornado --bind=0.0.0.0:$PORT app
worker: python worker.py

#web: NEW_RELIC_CONFIG_FILE=newrelic.ini ; newrelic-admin run-program gunicorn --workers=1 -k tornado app

# https://newrelic.com/docs/python/python-agent-and-uwsgi
#web: NEW_RELIC_CONFIG_FILE=newrelic.ini ; newrelic-admin run-program uwsgi --http-socket :$PORT --wsgi-file app.py
