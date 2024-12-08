import unittest
from main import (
    parse_yaml,
    convert_to_custom_language,
    convert_consts,
    convert_expression,
    process_comments

)


class TestConfigParser(unittest.TestCase):

    def test_parse_yaml_valid(self):
        input_text = """
        key: value
        number: 123
        """
        expected_result = {'key': 'value', 'number': 123}
        result = parse_yaml(input_text)
        self.assertEqual(result, expected_result)

    def test_parse_yaml_invalid(self):
        input_text = """
        key: value
        number: 123
        key2
        """
        with self.assertRaises(SystemExit):
            parse_yaml(input_text)

    def test_convert_to_custom_language_str(self):
        result = convert_to_custom_language("value")
        self.assertEqual(result, '"value"')

    def test_convert_to_custom_language_int(self):
        result = convert_to_custom_language(123)
        self.assertEqual(result, '123')

    def test_convert_to_custom_language_float(self):
        result = convert_to_custom_language(123.456)
        self.assertEqual(result, '123.456')

    def test_convert_to_custom_language_dict(self):
        input_data = {"key1": "value1", "key2": 42}
        expected_result = "@{\n  key1 = \"value1\";\n  key2 = 42;\n}"
        result = convert_to_custom_language(input_data)
        self.assertEqual(result, expected_result)

    def test_convert_to_custom_language_list(self):
        input_data = ["value1", 42, 3.14]
        expected_result = "[\"value1\" 42 3.14]"
        result = convert_to_custom_language(input_data)
        self.assertEqual(result, expected_result)

    def test_convert_consts(self):
        consts = {"PI": 3.14, "MAX": 100}
        expected_result = "  const PI = 3.14;\n  const MAX = 100;\n"
        result = convert_consts(consts)
        self.assertEqual(result, expected_result)

    def test_convert_expression_valid(self):
        consts = {"a": 10, "b": 20}
        expression = "^[a + b]"
        expected_result = "30"
        result = convert_expression(expression, consts)
        self.assertEqual(result, expected_result)


    def test_process_comments_single_line(self):
        input_text = """
        #hkbhblhkjbkjbhkjbj
        """
        expected_result = "//hkbhblhkjbkjbhkjbj"
        result = process_comments(input_text)
        self.assertEqual(result, expected_result)

    def test_process_comments_long_comment(self):
        input_text = """
        # gfggvgkjvkjhvuygvuykhgiygbiyulgihbilbiluihblihljnlkjbkljbklhbjkhvgkjvhgjvghcfjgchjchgv
        """
        expected_result = "+/gfggvgkjvkjhvuygvuykhgiygbiyulgihbilbiluihblihljnlkjbkljbklhbjkhvgkjvhgjvghcfjgchjchgv/+"
        result = process_comments(input_text)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
