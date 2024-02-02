from config import config
from unittest import TestCase

class ConfigUnitTests(TestCase):
    def test_no_arguments_should_throw(self):
        with self.assertRaises(ValueError):
            config()