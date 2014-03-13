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

task :deps => [:dev_env] do
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
  DEFAULT = SERVER
  DEFAULT = WORKER if not DEFAULT
  SYSTEM_URL = "http://app.herokuapp.com"
  SYSTEM_EMAIL = "no-reply@gmail.com"
  ADMIN_EMAIL = "paulocheque@gmail.com"
  BSALT = "yoursalt"
  GOOGLE_API_KEY = ""
  GOOGLE_CONSUMER_KEY = ""
  GOOGLE_CONSUMER_SECRET = ""
  FACEBOOK_API_KEY = ""
  FACEBOOK_SECRET = ""
  FACEBOOK_API_SECRET = ""
  TWITTER_API_KEY = ""
  TWITTER_API_SECRET = ""
  TWITTER_CONSUMER_KEY = ""
  TWITTER_CONSUMER_SECRET = ""
  TWITTER_ACCESS_TOKEN = ""
  TWITTER_ACCESS_TOKEN_SECRET = ""
  PAGSEGURO_EMAIL = ""
  PAGSEGURO_TOKEN = ""

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
    # sh "heroku addons:add postmark --app #{WORKER}" if WORKER
    # sh "heroku addons:add mongolab --app #{SERVER}" if SERVER
    # sh "heroku domains:add #{DOMAIN} --app #{SERVER}" if SERVER and DOMAIN
  end

  task :config => [] do
    sh "heroku config --app #{SERVER}" if SERVER
    sh "heroku config --app #{WORKER}" if WORKER
    sh "heroku ps --app #{SERVER}" if SERVER
    sh "heroku ps --app #{WORKER}" if WORKER
  end

  task :logs => [] do
    sh "heroku logs -n=10 --app #{SERVER}" if SERVER
    sh "heroku logs -n=10 --app #{WORKER}" if WORKER
  end

  task :console => [] do
    sh "heroku run python --app #{DEFAULT}"
  end

  task :report do
    sh "heroku run fab report --app #{DEFAULT}"
  end

  task :setvars do
    REDISTOGO_URL = `heroku config:get REDISTOGO_URL --app #{SERVER}` if SERVER
    REDISTOGO_URL.strip! if SERVER
    sh "heroku config:set REDIS_URL=#{REDISTOGO_URL} REDISTOGO_URL=#{REDISTOGO_URL} --app #{WORKER}" if WORKER

    MONGOHQ_URL = `heroku config:get MONGOHQ_URL --app #{SERVER}` if SERVER
    MONGOHQ_URL.strip! if SERVER
    sh "heroku config:set MONGOHQ_URL=#{MONGOHQ_URL} --app #{WORKER}" if WORKER

    [SERVER, WORKER].each { |app|
      if app
        sh "heroku config:set SYSTEM_URL=#{SYSTEM_URL} --app #{app}" if SYSTEM_URL != ""
        sh "heroku config:set SYSTEM_EMAIL=#{SYSTEM_EMAIL} --app #{app}" if SYSTEM_EMAIL != ""
        sh "heroku config:set ADMIN_EMAIL=#{ADMIN_EMAIL} --app #{app}" if ADMIN_EMAIL != ""
        sh "heroku config:set BSALT=#{BSALT} --app #{app}" if BSALT != ""

        sh "heroku config:set GOOGLE_CONSUMER_KEY=#{GOOGLE_CONSUMER_KEY} --app #{app}" if GOOGLE_CONSUMER_KEY != ""
        sh "heroku config:set GOOGLE_CONSUMER_SECRET=#{GOOGLE_CONSUMER_SECRET} --app #{app}" if GOOGLE_CONSUMER_SECRET != ""
        sh "heroku config:set FACEBOOK_API_KEY=#{FACEBOOK_API_KEY} --app #{app}" if FACEBOOK_API_KEY != ""
        sh "heroku config:set FACEBOOK_SECRET=#{FACEBOOK_SECRET} --app #{app}" if FACEBOOK_SECRET != ""
        sh "heroku config:set FACEBOOK_API_SECRET=#{FACEBOOK_API_SECRET} --app #{app}" if FACEBOOK_API_SECRET != ""
        sh "heroku config:set TWITTER_API_KEY=#{TWITTER_API_KEY} --app #{app}" if TWITTER_API_KEY != ""
        sh "heroku config:set TWITTER_API_SECRET=#{TWITTER_API_SECRET} --app #{app}" if TWITTER_API_SECRET != ""
        sh "heroku config:set TWITTER_CONSUMER_KEY=#{TWITTER_CONSUMER_KEY} --app #{app}" if TWITTER_CONSUMER_KEY != ""
        sh "heroku config:set TWITTER_CONSUMER_SECRET=#{TWITTER_CONSUMER_SECRET} --app #{app}" if TWITTER_CONSUMER_SECRET != ""
        sh "heroku config:set TWITTER_ACCESS_TOKEN=#{TWITTER_ACCESS_TOKEN} --app #{app}" if TWITTER_ACCESS_TOKEN != ""
        sh "heroku config:set TWITTER_ACCESS_TOKEN_SECRET=#{TWITTER_ACCESS_TOKEN_SECRET} --app #{app}" if TWITTER_ACCESS_TOKEN_SECRET != ""

        sh "heroku config:set PAGSEGURO_EMAIL=#{PAGSEGURO_EMAIL} --app #{app}" if PAGSEGURO_EMAIL != ""
        sh "heroku config:set PAGSEGURO_TOKEN=#{PAGSEGURO_TOKEN} --app #{app}" if PAGSEGURO_TOKEN != ""
      end
    }
  end

  task :deploy => [] do # :set_vars
    sh "git push heroku master"
    sh "heroku ps:scale web=1 --app #{SERVER}" if SERVER
    sh "heroku ps:scale worker=0 --app #{SERVER}" if SERVER

    sh "git push heroku2 master"
    sh "heroku ps:scale web=0 --app #{WORKER}" if WORKER
    sh "heroku ps:scale worker=1 --app #{WORKER}" if WORKER
  end
end

task :compress_js do
  sh "sudo npm install uglify-js -g"
  sh "uglifyjs static/js/*.js -o static/js/code.min.js --source-map code.min.js.map -p relative -c -m"
end

# brew install imagemagick
# http://www.imagemagick.org/Usage/resize/#resize
task :logos do
  # Square
  Dir.chdir("static/img") do
    LOGO_SQUARE = "logo-1024x1024.png"
    sh "convert #{LOGO_SQUARE} -resize 512x512\! logo-512x512.png" # FB logo
    sh "convert #{LOGO_SQUARE} -resize 180x180\! logo-180x180.png" # FB logo
    sh "convert #{LOGO_SQUARE} -resize 144x144\! logo-144x144.png"
    sh "convert #{LOGO_SQUARE} -resize 114x114\! logo-114x114.png"
    sh "convert #{LOGO_SQUARE} -resize 72x72\! logo-72x72.png"
    sh "convert #{LOGO_SQUARE} -resize 57x57\! logo-57x57.png"
    sh "convert #{LOGO_SQUARE} -resize 32x32\! logo-32x32.png" # favicon
    sh "convert #{LOGO_SQUARE} -resize 16x16\! logo-16x16.png" # favicon and FB app small logo
    # Mobile Portrait
    LOGO_PORTRAIT = "logo-1024x1024.png"
    sh "convert #{LOGO_PORTRAIT} -resize 1536x2008\! logo-1536x2008.png"
    sh "convert #{LOGO_PORTRAIT} -resize 640x1136\! logo-640x1136.png"
    sh "convert #{LOGO_PORTRAIT} -resize 768x1004\! logo-768x1004.png"
    sh "convert #{LOGO_PORTRAIT} -resize 640x960\! logo-640x960.png"
    sh "convert #{LOGO_PORTRAIT} -resize 320x480\! logo-320x480.png"
    # Mobile Landscape
    LOGO_LANDSCAPE = "logo-1024x1024.png"
    sh "convert #{LOGO_LANDSCAPE} -resize 2048x1496\! logo-2048x1496.png"
    sh "convert #{LOGO_LANDSCAPE} -resize 1024x748\! logo-1024x748.png"
    # Banners
    LOGO_BANNER = "logo-1024x1024.png"
    sh "convert #{LOGO_BANNER} -resize 800x150\! logo-800x150.png" # FB app cover image
    sh "convert #{LOGO_BANNER} -resize 400x150\! logo-400x150.png" # FB cover image
    sh "convert #{LOGO_BANNER} -resize 155x100\! logo-155x100.png" # FB app web banner
    sh "convert #{LOGO_BANNER} -resize 200x60\! logo-200x60.png" # Site logo
    sh "convert #{LOGO_BANNER} -resize 150x50\! logo-150x50.png" # Site logo
    sh "convert #{LOGO_BANNER} -resize 140x40\! logo-140x40.png" # Site logo
  end
end

task :all => [:dev_env, :deps, :tests]

task :default => [:tests]
