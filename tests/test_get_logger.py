import unittest
from pukr import get_logger


class TestGetLogger(unittest.TestCase):
    def test_no_file(self):
        """Tests instantiation without setting up a file sink"""
        log = get_logger(log_name='test')
        self.assertEqual(1, len(log._core.handlers.keys()))
