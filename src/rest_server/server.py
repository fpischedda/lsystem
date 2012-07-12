#! /usr/bin/python

# Simple REST server

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from rest_server import action_manager
from rest_server import session_manager
from rest_server import settings
from automation.automator import Automator

from collections import deque
import user_manager

import json

import sys

from daemon import Daemon

__author__="francescopischedda"
__date__ ="$30-dic-2011 13.15.26$"

class RESTServer(BaseHTTPRequestHandler):
    """
    Simple REST server to interface with game
    """

    def do_GET(self):
        """Handles the REST GET requests"""

        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            action, parameters = get_action(self.path)
            #self.wfile.write('action: %s <br/>' % action)

            #self.wfile.write('parameters: %s <br/>' % parameters)

            #self.wfile.write('response %s <br/>' % action_manager.handle_action(action, parameters))

            ret = action_manager.handle_action(action, parameters)
            self.wfile.write(json.dumps(ret, default=json_handler))
        except IOError:
            self.send_error(404, "unhandled request")

def json_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj
    
def get_action(query_string):
    """
    Action parser
    parameters:
    query_string: the requested query string to be parsed
    returns:
    the action name and the corresponding parameters dict
    """

    splitted = deque(query_string.split("/"))
    splitted.popleft()
    action_name = splitted.popleft()

    #get the action definition
    try:
        new_action = settings.Settings.get_instance().actions[action_name]

        #load the default definition of a function
        action = settings.Settings.get_instance().action_stub.copy()

        #merge defaults with user specified function properties
        action.update(new_action)

    except KeyError:
        return None, None

    #check if this action is login protected
    user_session = None
    if action["protected"] == True:

        sid = splitted.popleft()

        user_session = session_manager.get_instance().get_session(sid)

        if user_session is None:
            return None, None

    try:
        parameters = parse_parameters(action, splitted)
    except IndexError:
        return None, None
    
    parameters['session'] = user_session
    return action_name, parameters

def parse_parameters(action, parameter_list):
    """
    Parse the parameter list using the action name
    parameter:
    action: the name of the action
    parameter_list: list of parameters to be translated to a dict
    """

    params = dict()

    p = action["parameters"]
    for k in p:

        try:
            params[k['name']] = parameter_list[k['position']]
        except IndexError as ex:
            if k['optional'] == False:
                raise ex
            else:
                break

    return params

def start_server(port):

    try:
        server = HTTPServer(('', port), RESTServer)

        print('Starting automator thread 60 seconds interval')

        #automator will spleep for 60 seconds after each step<
        a = Automator(60)
        a.start()

        print('starting server at port %s' % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print('terminate signal received, shutting down...')
        server.socket.close()

        print('waiting for the automation thread to stop...')
        a.end()
        a.join()
        print('...done')

        print 'saving active users...'

        user_manager.get_instance().save_all_users()

        print '...done'

class MyDaemon(Daemon):

    def __init__(self, port):

        Daemon.__init__(self, "/tmp/lsystem-server-p%s.pid" % port)

        self.port = port
        
    def run(self):
	start_server(self.port)
 
if __name__ == "__main__":

    from optparse import OptionParser
    usage = "usage: %prog commands"
    parser = OptionParser(usage)

    parser.add_option("-s", "--settings",
                  dest="settings", default="settings/app.json",
                  help="specify settings file; default is settings/app.json")

    parser.add_option("-p", "--port",
                  dest="port", default="8000",
                  help="specify the port to listen; default is 8000")
                  
    (options, args) = parser.parse_args()
    settings.Settings.load_configuration(options.settings)

    if len(args) >= 1:

        daemon = MyDaemon(options.port)
        
        if 'start' == args[0]:
                daemon.start()
        elif 'stop' == args[0]:
                daemon.stop()
        elif 'restart' == args[0]:
                daemon.restart()
        else:
                print "Unknown command"
                sys.exit(2)
        sys.exit(0)
    else:
        start_server(8000)
            #print "usage: %s start|stop|restart" % sys.argv[0]
            #sys.exit(2)
