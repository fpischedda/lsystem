# Simple REST server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import sys
from daemon import Daemon
import settings
import session_manager
import url_action_caller


class RESTServer(BaseHTTPRequestHandler):
    """
    Simple REST server to interface with game
    """

    def do_GET(self):
        """Handles the REST GET requests"""

        try:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

            try:
                ret = url_action_caller.call_by_url(self.path,
                                                    self,
                                                    session_manager.get_session)

                self.wfile.write(json.dumps(ret))
            except url_action_caller.AuthException:
                self.send_error(403, "auth error")

        except IOError:
            self.send_error(404, "unhandled request")


def start_server(port, actions_dict):

    url_action_caller.init(actions_dict, 'actions')

    try:
        s = HTTPServer(('', port), RESTServer)

        print('starting server at port %s' % port)
        s.serve_forever()

    except KeyboardInterrupt:
        print('terminate signal received, shutting down...')
        s.socket.close()

        print '...done'


class MyDaemon(Daemon):

    def __init__(self, port):

        Daemon.__init__(self, "/tmp/lsystem-server-p%s.pid" % port)

        self.port = port

    def run(self):
        s = settings.Settings.get_instance()
        start_server(self.port, s.actions)

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
        s = settings.Settings.get_instance()
        start_server(8000, s.actions)
