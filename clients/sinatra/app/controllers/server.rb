require 'sinatra'
require 'rest_client'
require 'json'

SiteConfig = OpenStruct.new(
                 :title => 'Dev Francesco Pischedda',
                 :author => 'Francesco Pischedda',
                 :url_base => 'http://localhost:4567/')

module LSystem
  class Web < Sinatra::Base

    configure do
      set :public_folder, "#{File.dirname(__FILE__)}/../public"
      set :views, "#{File.dirname(__FILE__)}/../views"
    end

    enable :sessions

    def session!
      if session[:sid].nil? then redirect '/login' end
    end
    
    def session?
      not session[:sid].nil?
    end
    
    def session_end!
      
      session.delete(:username)
      session.delete(:sid)
    end
    
    get '/' do
      session!
      erb :index
    end
    
    get '/logout' do

      session!
      
      @username = session[:username]
      session_end!
      erb :logout
    end
    
    get '/login*' do
      
      if session?
        redirect '/'
      else
        erb :login
      end
    end
    
    post '/register*' do

      response = RestClient.send(:get, "http://localhost:8000/register/#{params[:username]}/#{params[:password]}/#{params[:email]}", nil) 

      if response.code == 200
        result = JSON.parse(response.to_str)

        if result['result'] == 'OK'

          session[:username] = params[:username]
          session[:sid] = result["session_id"]
          # "{'result':'OK'}"
          redirect '/'
        else
          session_end!
          @reason = result['reason']
          erb :login
          # "{'result':'KO', 'reason':#{result['reason']}}"
        end
      else
        "{'result':'KO','reason':'HTTP-CODE:#{response.code}}"
      end

    end

    post '/login*' do

      response = RestClient.send(:get, "http://localhost:8000/login/#{params[:email]}/#{params[:password]}", nil) 

      if response.code == 200
        result = JSON.parse(response.to_str)

        if result['result'] == 'OK'

          session[:username] = result['username']
          session[:sid] = result["session_id"]
          # "{'result':'OK'}"
          redirect '/'
        else
          session_end!
          @reason = result['reason']
          erb :login
          # "{'result':'KO', 'reason':#{result['reason']}}"
        end
      else
        "{'result':'KO','reason':'HTTP-CODE:#{response.code}}"
      end

    end

    get '/*/auth*' do

      if session?
        path = request.path_info.sub('auth', session[:sid])
        RestClient.send(:get, "http://localhost:8000#{path}", nil)
      else
        "{'result':'KO','reason':'unauthorized request'}" + session.inspect
      end
      #erb :index
    end

    get '/*' do
      RestClient.send(:get, "http://localhost:8000#{request.path_info}", nil) 
    end
  end
end
