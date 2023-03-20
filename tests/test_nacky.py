import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nacky.nacky import initial_setup, connection_setup, reset
from nacky.check_dependencies import check_dependencies

class TestNacky(unittest.TestCase):

    def test_check_dependencies(self):
        # Test if all required tools are installed
        result = check_dependencies()
        self.assertTrue(result, "Dependencies check failed. Make sure all required tools are installed.")

    def test_initial_setup(self):
        # Test if the initial setup function returns the expected result
        # You may need to adjust the test parameters based on your specific implementation
        result = initial_setup("eth0", "eth1")
        self.assertIsNotNone(result, "Initial setup failed.")

    def test_connection_setup(self):
        # Test if the connection setup function returns the expected result
        # You may need to adjust the test parameters based on your specific implementation
        result = connection_setup("eth0", "eth1", "00:11:22:33:44:55")
        self.assertIsNotNone(result, "Connection setup failed.")

    def test_reset(self):
        # Test if the reset function returns the expected result
        result = reset("eth0")
        self.assertIsNotNone(result, "Reset failed.")

if __name__ == '__main__':
    unittest.main()