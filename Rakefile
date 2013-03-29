
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

task :install => [] do
  sh "python --version"
  sh "ruby --version"
  sh "easy_install pip"
  sh "virtualenv venv"
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

task :test => [] do
  sh "nosetests"
end

task :load_test => [] do
  sh "multimech-run tests/load-test"
  sh "python tests/benchmarks/your_file.py"
end

task :heroku => [] do
  sh "heroku config"
end

task :deploy => [] do
  sh "git push heroku master"
end

task :default => [:server]
