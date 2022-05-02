import pathlib
import tempfile
import unittest
from pukr import get_logger


class TestGetLogger(unittest.TestCase):
    def test_no_file(self):
        """Tests instantiation without setting up a file sink"""
        log = get_logger(log_name='test')
        self.assertEqual(1, len(log._core.handlers.keys()))

    def test_with_file(self):
        """Tests instantiation without setting up a file sink"""
        mock_path = pathlib.Path(tempfile.gettempdir())
        log = get_logger(log_name='test', log_dir_path=mock_path)
        self.assertEqual(2, len(log._core.handlers.keys()))
        self.assertTrue(mock_path.joinpath('test.log').exists())
