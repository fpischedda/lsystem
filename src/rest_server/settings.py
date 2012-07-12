import json
import logging
import sys

#! /usr/bin/python

# legge i settaggi dell'applicazione da un file di configurazione


class Settings:

    __instance = None

    def __init__(self, filename='settings/app.json'):

        #setto la configurazione di base che verra' eventualmente
        #sovrascritta da quella del file di configurazione
        self.configuration_file = filename

        self.actions = {}
        self.action_stub = {}
        self.log_filename = './log.txt'
        
        try:
            f = open(filename)

            conf = f.read()
            f.close()

            conf_obj = json.loads(conf)

            self.actions = conf_obj['actions']
            self.action_stub = conf_obj['action_stub']
            
        except:
            logging.warning("error while reading settings file %s nella lettura del file di configurazione: %s" % (filename, str(sys.exc_info())))
        finally:
            #set the logging level to debug
            logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=self.log_filename,
                    filemode='a')
    @staticmethod
    def load_configuration(filename='settings/app.json'):

        Settings.__instance = Settings(filename)

        return Settings.__instance

    @staticmethod
    def get_instance():

        if Settings.__instance == None:

            Settings.load_configuration()

        return Settings.__instance

    def __repr__(self):

        dict = {'log_filename':self.log_filename, 'actions':self.actions,
            'action_stub':self.action_stub}
            
        return json.dumps(dict, sort_keys=True, indent=4)

__author__="francescopischedda"
__date__ ="$23-feb-2011 10.02.55$"

if __name__ == "__main__":

    s = Settings.load_configuration('settings/app.json')

    print( repr(s))
