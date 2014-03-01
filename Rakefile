PYTHON = "2.7"
# PYTHON = "3.3"

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

def virtual_env(command, env="env#{PYTHON}")
  sh "source #{env}/bin/activate && #{command}"
end

def create_virtual_env(dir, python)
  sh "virtualenv #{dir} -p #{python}"
end

task :clean => [] do
  sh "rm -rf ~*"
  sh "find . -name '*.pyc' -delete"
  sh "rm -rf data/"
  sh "rm -rf *.egg-info"
  sh "rm -rf dist/"
end

task :install => [] do
  sh "python --version"
  sh "ruby --version"
  sh "easy_install pip"
  sh "brew install mongo"
  sh "brew install redis"
end

task :dev_env => [] do
  create_virtual_env("env#{PYTHON}", "python#{PYTHON}")
end

task :dependencies => [:dev_env] do
  virtual_env("pip install -r requirements.txt")
  virtual_env("pip install -r requirements-test.txt")
end

task :tests => [] do # no dependencies for performance
  virtual_env("nosetests")
end

task :server => [] do
  virtual_env("foreman start")
end

task :mongo => [] do
  sh "mkdir -p data/db"
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

namespace :heroku do
  SERVER = "server"
  WORKER = "worker"
  DOMAIN = nil

  task :create => [] do
    # sh "heroku apps:create #{SERVER}" if SERVER
    # sh "heroku apps:create #{WORKER}" if WORKER
    sh "heroku addons:add newrelic --app #{SERVER}" if SERVER
    sh "heroku addons:add newrelic --app #{WORKER}" if WORKER
    # sh "newrelic-admin generate-config YOUR_ID newrelic.ini"
    sh "heroku addons:add papertrail --app #{SERVER}" if SERVER
    sh "heroku addons:add papertrail --app #{WORKER}" if WORKER
    # sh "heroku addons:add loggly --app #{SERVER}" if SERVER
    # sh "heroku addons:add loggly --app #{WORKER}" if WORKER
    sh "heroku addons:add redistogo --app #{SERVER}" if SERVER
    sh "heroku addons:add mongohq --app #{SERVER}" if SERVER
    sh "heroku addons:add scheduler --app #{WORKER}" if WORKER
    sh "heroku addons:add sendgrid --app #{WORKER}" if WORKER
    # sh "heroku addons:add mongolab --app #{SERVER}" if SERVER
    # sh "heroku domains:add #{DOMAIN} --app #{SERVER}" if SERVER and DOMAIN
  end

  task :status => [] do
    sh "heroku login"
    sh "heroku config --app #{SERVER}" if SERVER
    sh "heroku config --app #{WORKER}"

    sh "heroku ps --app #{SERVER}" if SERVER
    sh "heroku ps --app #{WORKER}"
    sh "heroku open"
    sh "heroku logs -t -p worker"
  end

  task :logs => [] do
    sh "heroku logs --tail --app #{SERVER}" if SERVER
    sh "heroku logs --tail --app #{WORKER}"
  end

  task :console => [] do
    sh "heroku run python --app #{WORKER}" if WORKER
  end

  task :deploy => [] do
    REDISTOGO_URL = `heroku config:get REDISTOGO_URL --app #{SERVER}` if SERVER
    REDISTOGO_URL.strip! if SERVER
    sh "heroku config:set REDIS_URL=#{REDISTOGO_URL} REDISTOGO_URL=#{REDISTOGO_URL} --app #{WORKER}" if WORKER

    MONGOHQ_URL = `heroku config:get MONGOHQ_URL --app #{SERVER}` if SERVER
    MONGOHQ_URL.strip! if SERVER
    sh "heroku config:set MONGOHQ_URL=#{MONGOHQ_URL} --app #{WORKER}" if WORKER

    sh "git push heroku master"
    sh "heroku ps:scale web=1 --app #{SERVER}" if SERVER
    sh "heroku ps:scale worker=0 --app #{SERVER}" if SERVER

    sh "git push heroku2 master"
    sh "heroku ps:scale web=0 --app #{WORKER}" if WORKER
    sh "heroku ps:scale worker=1 --app #{WORKER}" if WORKER

    sh "heroku ps --app #{SERVER}" if SERVER
    sh "heroku ps --app #{WORKER}" if WORKER
    sh "heroku config --app #{SERVER}" if SERVER
    sh "heroku config --app #{WORKER}" if WORKER
  end

  task :report do
    APP = SERVER
    APP = WORKER if not APP
    sh "heroku run fab report --app #{APP}"
  end
end

task :compress_js do
  sh "sudo npm install uglify-js -g"
  sh "uglifyjs static/js/*.js -o static/js/code.min.js --source-map code.min.js.map -p relative -c -m"
end

task :all => [:dev_env, :dependencies, :tests]

task :default => [:tests]
