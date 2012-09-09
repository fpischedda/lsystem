###
# Francesco Pischedda
# read settings from the specified JSON file
# a default configuration is set
###
import json
import logging
import sys


class Settings:

    __instance = None

    __default_settings = { 
                    "actions": {}, 
                    "action_stub": {}, 
                    "log_filename": './log.txt'}

    def __init__(self):

        self.configuration_file = None
        self.settings = Settings.__default_settings.copy()

    def __init__(self, filename):

        #setto la configurazione di base che verra' eventualmente
        #sovrascritta da quella del file di configurazione
        self.configuration_file = filename

        self.settings = Settings.__default_settings.copy()

        try:
            f = open(filename)

            conf = f.read()
            f.close()

            conf_obj = json.loads(conf)

            self.update(conf_obj)

        except:
            logging.warning("error while reading settings file %s nella lettura del file di configurazione: %s" % (filename, str(sys.exc_info())))
        finally:
            #set the logging level to debug
            logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=self.settings["log_filename"],
                    filemode='a')

    def __getattr__(self, name):

        try:
            return self.settings[name]
        except:
            raise AttributeError("setting %s not found" % name)

    @staticmethod
    def load_configuration(filename='settings/app.json'):

        Settings.__instance = Settings(filename)

        return Settings.__instance

    @staticmethod
    def get_instance():

        if Settings.__instance == None:

            Settings.load_configuration()

        return Settings.__instance

    @staticmethod
    def default_settings():
        return Settings.__default_settings
    def __repr__(self):

        return json.dumps(elf.settings, sort_keys=True, indent=4)

__author__="francescopischedda"
__date__ ="$23-feb-2011 10.02.55$"

if __name__ == "__main__":

    s = Settings.load_configuration('settings/app.json')

    print( repr(s))
