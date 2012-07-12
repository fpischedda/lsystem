# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="francescopischedda"
__date__ ="$26-feb-2012 21.48.23$"

import messaging.timeline

def last_messages(parameters):

    try:
        last_id = int(parameters['last_id'])
        ret = messaging.timeline.last_messages_by_last_id(last_id)
    except KeyError:
        ret = messaging.timeline.last_messages(40)
    except ValueError:
        ret = messaging.timeline.last_messages(40)

    return {'result':'OK', 'timeline':ret}

if __name__ == "__main__":
    print "Hello World"
