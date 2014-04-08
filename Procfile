# https://docs.newrelic.com/docs/python/
# https://docs.newrelic.com/docs/python/python-agent-and-heroku

# Without NewRelic
#web: gunicorn -k tornado --bind=0.0.0.0:$PORT app

# With NewRelic
web: newrelic-admin run-program gunicorn -k tornado --bind=0.0.0.0:$PORT app
#web: newrelic-admin run-program uwsgi --http-socket :$PORT --wsgi-file app.py

# Worker
worker: python worker.py
