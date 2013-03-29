
def colorize(text, color)
  color_codes = {
    :black    => 30,
    :red      => 31,
    :green    => 32,
    :yellow   => 33,
    :blue     => 34,
    :magenta  => 35,
    :cyan     => 36,
    :white    => 37
  }
  code = color_codes[color]
  if code == nil
    text
  else
    "\033[#{code}m#{text}\033[0m"
  end
end

task :clean => [] do
  sh "rm -rf *.pyc *.pyo"
  sh "rm -rf data"
end

task :install => [] do
  sh "python --version"
  sh "ruby --version"
  sh "easy_install pip"
  sh "virtualenv venv --distribute"
  # sh "source venv/bin/activate"
  sh "pip install -r requirements.txt"
  # sh "pip install -r requirements-test.txt"
  sh "brew install mongo"
  sh "brew install redis"
end

task :server => [] do
  # sh "source venv/bin/activate"
  sh "foreman start"
  #sh "python app.py"
end

task :mongo => [] do
  sh "mongod --dbpath=data/db"
end

task :redis => [] do
  sh "redis-server"
end

task :scheduler => [] do
  sh "rqscheduler"
end

task :dashboard => [] do
  sh "rq-dashboard"
end

task :monitor => [] do
  sh "redis-cli info"
  sh "redis-cli ping"
  # sh "redis-cli (get key) (set key value)"
end

task :test => [] do
  sh "nosetests"
end

task :load_test => [] do
  # sh "multimech-newproject tests/load-test"
  sh "multimech-run tests/load-test"
  sh "python tests/benchmarks/your_file.py"
end

task :heroku => [] do
  sh "heroku login"
  sh "heroku config"

  # heroku apps:create YOUR_APP
  # heroku addons:add newrelic
  # newrelic-admin generate-config YOUR_ID newrelic.ini
  # heroku addons:add papertrail
  # heroku addons:add loggly
  # heroku addons:add redistogo
  # heroku domains:add YOUR_DOMAIN

  # heroku ps:scale web=1
  # heroku ps
  # heroku open
  # heroku logs
  # heroku logs -t -p worker
  # heroku run python
end

task :deploy => [] do
  sh "git push heroku master"
end

task :default => [:server]
