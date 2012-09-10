import unittest
from rest_server.settings import Settings

class TestDefaultSettings(unittest.TestCase):

    def test_default_settings(self):

        s = Settings()

        defaults = Settings.default_settings()

        self.assertEqual(defaults["action_stub"],s.action_stub)
        self.assertEqual(defaults["actions"], s.actions)
        self.assertEqual(defaults["log_filename"], s.log_filename)

class TestSettingsLoadingFailure(unittest.TestCase):

    def test_load_configuration_fail(self):

        self.assertRaises(Exception, Settings.load_configuration,'bogusfile')

class TestAccessNonExistentSetting(unittest.TestCase):

    def test_access_nonexistent_setting(self):
        
        s = Settings()

        self.assertRaises(AttributeError,s.__getattr__,"impossible_setting")

if __name__ == "__main__":
    
    unittest.main()

