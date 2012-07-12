#========================
#CONFIG
#========================
set :application, "APP_NAME"
 
set :scm, :git
set :git_enable_submodules, 1
set :repository, "GIT_URL"
set :branch, "master"
set :ssh_options, { :forward_agent => true }
 
set :stage, :production
set :user, "deploy"
set :use_sudo, false
set :runner, "deploy"
set :deploy_to, "/data/apps/#{stage}/#{application}"
set :app_server, :passenger
set :domain, "DOMAIN_URL"
 
#========================
#ROLES
#========================
role :app, domain
role :web, domain
role :db, domain, :primary => true

#========================
#CUSTOM
#========================
 
namespace :deploy do
  task :start, :roles => :app do
    run "touch #{current_release}/tmp/restart.txt"
  end
 
  task :stop, :roles => :app do
    # Do nothing.
  end
 
  desc "Restart Application"
  task :restart, :roles => :app do
    run "touch #{current_release}/tmp/restart.txt"
  end
end
