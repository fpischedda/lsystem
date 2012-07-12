ENV["RACK_ENV"] ||= "development"

require 'bundler'
Bundler.setup

Bundler.require(:default, ENV["RACK_ENV"].to_sym)

Dir["./lib/**/*.rb"].each { |f| require f }
Dir["./app/controllers/**/*.rb"].each { |f| require f }

FileUtils.mkdir_p 'log' unless File.exists?('log')
log = File.new("log/sinatra.log", "a")
$stdout.reopen(log)
$stderr.reopen(log)

use Rack::ShowExceptions
use Rack::ContentLength
use Rack::Static, :urls => [ '/favicon.ico', '/stylesheets', '/js', '/images' ], :root => "public"
use Rack::Session::Cookie, :key => 'dev_imcode_in',
                           :path => '/',
                           :expire_after => 2592000, # In seconds
                           :secret => '3&4if$32+'
use Rack::Session::Pool
