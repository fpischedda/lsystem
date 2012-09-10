import unittest
from rest_server.settings import Settings

class TestDefaultSettings(unittest.TestCase):

    def test_default_settings(self):
        '''
            tests that the default settings are known
        '''
        s = Settings()

        defaults = Settings.default_settings()

        self.assertEqual(defaults["action_stub"],s.action_stub)
        self.assertEqual(defaults["actions"], s.actions)
        self.assertEqual(defaults["log_filename"], s.log_filename)

class TestSettingsLoadingFailure(unittest.TestCase):

    def test_load_configuration_fail(self):
        '''
            tests that an exception is raised when trying to load a
            settings file that doesn't exists
        '''
        self.assertRaises(Exception, Settings.load_configuration,'bogusfile')

class TestAccessNonExistentSetting(unittest.TestCase):

    def test_access_nonexistent_setting(self):
        '''
            tests that an exception of the type AttributeError
            is raised when accessing a non existent setting
        '''
        s = Settings()

        self.assertRaises(AttributeError,s.__getattr__,"impossible_setting")

class TestLoadingGoodSettings(unittest.TestCase):

    def test_loading_good_settings_file(self):
        '''
            tests the loading of a good settings file
        '''

        #load the default testing settings file which is in the
        #same directory of this test file
        
        import os
        path = os.path.dirname(os.path.abspath(__file__))

        filename = "{0}/default.json".format(path)

        s = Settings.load_configuration(filename)

        action_stub = {
                "function":"",
                "parameters":[],
                "protected":True
                }
        self.assertEqual(action_stub, s.action_stub)

        actions = {
            "test_func":{
                "function":"test.func",
                "parameters":[
                    {
                        "name":"parameter1",
                        "position":0, 
                        "optional":False
                    }
                ],
                "protected":False
            }
        }
        self.assertEqual(actions, s.actions)

        log_filename = "some_logfile"
        self.assertEqual(log_filename, s.log_filename)

if __name__ == "__main__":
    
    unittest.main()

