"""
Unit tests
"""

import unittest
from script import custom_function


class TestCustomFunction(unittest.TestCase):
    def test_custom_function_with_input(self):
        """
        Test custom_function with a specific input
        """
        input_value = "test_input"
        expected_output = "Custom function output: test_input"
        self.assertEqual(custom_function(input_value), expected_output)

    def test_custom_function_with_default_value(self):
        """
        Test custom_function with the default value
        """
        input_value = "default_value"
        expected_output = "Custom function output: default_value"
        self.assertEqual(custom_function(input_value), expected_output)


if __name__ == "__main__":
    unittest.main()
