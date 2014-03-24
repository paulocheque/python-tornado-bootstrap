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
  DEFAULT = SERVER
  DEFAULT = WORKER if not DEFAULT
  DOMAIN = "#{SERVER}.herokuapp.com"
  PROTOCOL = "http"
  ENV_VARS = {
    # TEST_MODE: "", # disabled
    # ASYNC_TASKS: "true", # active by default
    DATE_FORMAT: "%Y-%m-%d",
    TIME_FORMAT: "%H:%M",
    DATETIME_FORMAT: "\"%Y-%m-%d %H:%M\"",

    SYSTEM_NAME: "MyApp",
    DOMAIN: "#{DOMAIN}",
    PROTOCOL: "#{PROTOCOL}",
    SYSTEM_URL: "#{PROTOCOL}://#{DOMAIN}",
    SYSTEM_EMAIL: "no-reply@#{DOMAIN}",
    ADMIN_EMAIL: "paulocheque@gmail.com",
    BSALT: "#{DOMAIN}-yoursalt",

    GOOGLE_ANALYTICS: "", # UA-CHANGEHERE-1
    GOOGLE_PLUS_ACCOUNT: "",
    GOOGLE_API_KEY: "",
    GOOGLE_CONSUMER_KEY: "",
    GOOGLE_CONSUMER_SECRET: "",

    FACEBOOK_ACCOUNT: "",
    FACEBOOK_REDIRECT_URL: "#{PROTOCOL}://#{DOMAIN}/auth/facebook",
    FACEBOOK_API_KEY: "",
    FACEBOOK_SECRET: "",
    FACEBOOK_API_SECRET: "", # FACEBOOK_SECRET

    TWITTER_ACCOUNT: "",
    TWITTER_API_KEY: "",
    TWITTER_API_SECRET: "",
    TWITTER_CONSUMER_KEY: "", # TWITTER_API_KEY
    TWITTER_CONSUMER_SECRET: "", # TWITTER_API_SECRET
    TWITTER_ACCESS_TOKEN: "",
    TWITTER_ACCESS_TOKEN_SECRET: "",

    GITHUB_ACCOUNT: "",
    GITHUB_REDIRECT_URL: "#{PROTOCOL}://#{DOMAIN}/auth/github",
    GITHUB_CLIENT_ID: "",
    GITHUB_SECRET: "",
    GITHUB_SCOPE: "",

    SKYPE_ACCOUNT: "",

    PAGSEGURO_MODE: "live",
    PAGSEGURO_EMAIL: "",
    PAGSEGURO_TOKEN: "",
    MERCADOPAGO_MODE: "live",
    MERCADOPAGO_CLIENT_ID: "",
    MERCADOPAGO_CLIENT_SECRET: "",
    PAYPAL_MODE: "live",
    PAYPAL_CLIENT_ID: "",
    PAYPAL_CLIENT_SECRET: "",
    MOIP_MODE: "producao",
    MOIP_TOKEN: "",
    MOIP_KEY: "",
  }

  task :create => [] do
    # sh "git remote add bootstrap git@github.com:paulocheque/python-tornado-bootstrap.git"
    # sh "git pull bootstrap master"
    sh "heroku apps:create #{SERVER}" if SERVER
    sh "heroku apps:create #{WORKER}" if WORKER
    sh "git remote add heroku git@heroku.com:#{SERVER}.git" if SERVER
    sh "git remote add heroku2 git@heroku.com:#{WORKER}.git" if WORKER

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
    sh "heroku domains:add #{DOMAIN} --app #{SERVER}" if SERVER and not ENV_VARS[:DOMAIN].end_with?("herokuapp.com")
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
    redistogo_url = `heroku config:get REDISTOGO_URL --app #{SERVER}` if SERVER
    redistogo_url.strip! if SERVER
    mongohq_url = `heroku config:get MONGOHQ_URL --app #{SERVER}` if SERVER
    mongohq_url.strip! if SERVER

    [SERVER, WORKER].each { |app|
      if app
        vars = ENV_VARS.map{ |k,v| "#{k}=#{v}" }.join(' ')
        puts vars
        if app == WORKER
          complement = " REDIS_URL=#{redistogo_url} REDISTOGO_URL=#{redistogo_url} MONGOHQ_URL=#{mongohq_url}"
          vars = vars + complement
        end
        sh "heroku config:set #{vars} --app #{app}"
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
