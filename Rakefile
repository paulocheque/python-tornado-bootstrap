
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

task :test => [] do
  sh "nosetests"
end

task :load_test => [] do
  # sh "multimech-newproject tests/load-test"
  sh "multimech-run tests/load-test"
  sh "python tests/benchmarks/your_file.py"
end

task :heroku_create => [] do
  app = nil
  domain = nil
  sh "heroku apps:create #{app}" if app
  sh "heroku addons:add newrelic"
  # sh "newrelic-admin generate-config YOUR_ID newrelic.ini"
  sh "heroku addons:add papertrail"
  sh "heroku addons:add loggly"
  sh "heroku addons:add redistogo"
  sh "heroku addons:add mongohq"
  # sh "heroku addons:add mongolab"
  sh "heroku domains:add #{domain}" if domain
end

task :heroku => [] do
  sh "heroku login"
  sh "heroku config"

  sh "heroku ps:scale web=1"
  sh "heroku ps"
  sh "heroku open"
  sh "heroku logs"
  sh "heroku logs -t -p worker"
  # sh "heroku run python"
end

task :deploy => [] do
  sh "git push heroku master"
end

task :default => [:server]
