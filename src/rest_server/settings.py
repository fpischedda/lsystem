###
# Francesco Pischedda
# read settings from the specified JSON file
# a default configuration is set
###
import json
import logging


class Settings:

    __instance = None

    __default_settings = {"actions": {},
                          "action_stub": {},
                          "log_filename": './log.txt'}

    def __init__(self, filename=None):

        self.configuration_file = filename

        self.settings = Settings.__default_settings.copy()

        if filename is None:
            return

        try:
            f = open(filename)

            conf = f.read()
            f.close()

            conf_obj = json.loads(conf)
            #merge the base settings with those provided by
            #the configuration file
            self.settings.update(conf_obj)

        except Exception as e:
            raise e
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

        if Settings.__instance is None:

            Settings.load_configuration()

        return Settings.__instance

    @staticmethod
    def default_settings():
        return Settings.__default_settings

    def __repr__(self):

        return json.dumps(self.settings, sort_keys=True, indent=4)

__author__ = "francescopischedda"
__date__ = "$23-feb-2011 10.02.55$"

if __name__ == "__main__":

    s = Settings.load_configuration('settings/app.json')

    print(repr(s))
