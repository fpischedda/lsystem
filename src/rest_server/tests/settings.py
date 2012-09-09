import unittest
from rest_server.settings import Settings

class TestDefaultSettings(unittest.TestCase):

    def test_default_settings(self):

        s = Settings()

        defaults = Settings.default_settings()

        self.assertEqual(defaults["action_stub"],s.action_stub)
        self.assertEqual(defaults["actions"], s.actions)
        self.assertEqual(defaults["log_filename"], s.log_filename)

if __name__ == "__main__":
    
    unittest.main()

