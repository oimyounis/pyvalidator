import unittest

from .validator import Validator


WHITE_SPACES = "    "
BLANK = ''


def build_validator(data, rules):
    validator = Validator(data, rules)
    return validator.valid()


class RequiredRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': 'value'}
        rules = {'field': 'required'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': WHITE_SPACES}
        rules = {'field': 'required'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': BLANK}
        rules = {'field': 'required'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': None}
        rules = {'field': 'required'}
        self.assertFalse(build_validator(data, rules))


class EmailRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': 'mail@mail.com'}
        rules = {'field': 'email'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': 'mail@mail.com.co'}
        rules = {'field': 'email'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field': BLANK}
        rules = {'field': 'email'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field': None}
        rules = {'field': 'email'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': 'mail'}
        rules = {'field': 'email'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': 'mail@mail'}
        rules = {'field': 'email'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field': 'mail@mail.'}
        rules = {'field': 'email'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid4(self):
        data = {'field': WHITE_SPACES}
        rules = {'field': 'email'}
        self.assertFalse(build_validator(data, rules))


class NumericRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': '123'}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': '123.321'}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field': '123e5'}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field': '-123'}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field': '-123.321'}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field': '-123e5'}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field': 123}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field': 123.321}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid9(self):
        data = {'field': 123e5}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid10(self):
        data = {'field': -123}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid11(self):
        data = {'field': -123.321}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid12(self):
        data = {'field': -123e5}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid13(self):
        data = {'field': BLANK}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid14(self):
        data = {'field': 123e-5}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid15(self):
        data = {'field': -123e-5}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_valid16(self):
        data = {'field': None}
        rules = {'field': 'numeric'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': 'value'}
        rules = {'field': 'numeric'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': '123value'}
        rules = {'field': 'numeric'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field': WHITE_SPACES}
        rules = {'field': 'numeric'}
        self.assertFalse(build_validator(data, rules))


class InRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': '3'}
        rules = {'field': 'in:9,7,3,45'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': '56.5'}
        rules = {'field': ' in : 9 , 56.5 ,7 ,3,45 '}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field': 'two'}
        rules = {'field': 'in:one,two,three'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field': BLANK}
        rules = {'field': 'in:one,two,three'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field': None}
        rules = {'field': 'in:one,two,three'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field': 3}
        rules = {'field': 'in:3,6,8,1,10e-2'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': WHITE_SPACES}
        rules = {'field': 'in:one,two,three'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': 'four'}
        rules = {'field': 'in:one,two,three'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field': '3'}
        rules = {'field': 'in:3.5,6,8,1,10e-2'}
        self.assertFalse(build_validator(data, rules))


class MaxRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': 6}
        rules = {'field': 'max:8'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': 6}
        rules = {'field': 'max:6'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field': 'word'}
        rules = {'field': 'max:7'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field': 'word'}
        rules = {'field': 'max:4'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field': [1, 2, 3, 4, 5]}
        rules = {'field': 'max:10'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field': [6, 7, -8, 9, -10]}
        rules = {'field': 'max:5'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field': (1, 2, 3, 4, 5)}
        rules = {'field': 'max:10'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field': (6, 7, -8, 9, -10)}
        rules = {'field': 'max:5'}
        self.assertTrue(build_validator(data, rules))

    def test_valid9(self):
        data = {'field': '15645'}
        rules = {'field': 'max:6'}
        self.assertTrue(build_validator(data, rules))

    def test_valid10(self):
        data = {'field': None}
        rules = {'field': 'max:8'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': 15}
        rules = {'field': 'max:8'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': 15}
        rules = {'field': 'max:14.5'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field': 15.5}
        rules = {'field': 'max:15'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid4(self):
        data = {'field': '15.5'}
        rules = {'field': 'max:3'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid5(self):
        data = {'field': 'word word'}
        rules = {'field': 'max:7'}
        self.assertFalse(build_validator(data, rules))

    # def test_invalid6(self):  # This will throw a ValueError exception
    #     data = {'field': 'word word'}
    #     rules = {'field': 'max:invalid'}
    #     self.assertFalse(build_validator(data, rules))

    def test_invalid7(self):
        data = {'field': [1, 2, 3, 4, 5, 6]}
        rules = {'field': 'max:5'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid8(self):
        data = {'field': (1, 2, 3, 4, 5, 6)}
        rules = {'field': 'max:4'}
        self.assertFalse(build_validator(data, rules))


class MinRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': 6}
        rules = {'field': 'min:5'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': 6}
        rules = {'field': 'min:6'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field': 'word'}
        rules = {'field': 'min:3'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field': 'word'}
        rules = {'field': 'min:4'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field': [1, 2, 3, 4, 5, 6]}
        rules = {'field': 'min:5'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field': [6, 7, -8, 9, -10]}
        rules = {'field': 'min:5'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field': (1, 2, 3, 4, 5, 6, 7, 8)}
        rules = {'field': 'min:0'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field': (6, 7, -8, 9, -10)}
        rules = {'field': 'min:5'}
        self.assertTrue(build_validator(data, rules))

    def test_valid9(self):
        data = {'field': '15645'}
        rules = {'field': 'min:4'}
        self.assertTrue(build_validator(data, rules))

    def test_valid10(self):
        data = {'field': None}
        rules = {'field': 'min:8'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': 15}
        rules = {'field': 'min:25'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': 14}
        rules = {'field': 'min:14.5'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field': 14.99}
        rules = {'field': 'min:15'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid4(self):
        data = {'field': '15.5'}
        rules = {'field': 'min:9'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid5(self):
        data = {'field': 'word word'}
        rules = {'field': 'min:13'}
        self.assertFalse(build_validator(data, rules))

    # def test_invalid6(self):  # This will throw a ValueError exception
    #     data = {'field': 'word word'}
    #     rules = {'field': 'min:invalid'}
    #     self.assertFalse(build_validator(data, rules))

    def test_invalid7(self):
        data = {'field': [1, 2, "word", 6]}
        rules = {'field': 'min:5'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid8(self):
        data = {'field': (1, 2, 3, 4, 5, 6)}
        rules = {'field': 'min:7'}
        self.assertFalse(build_validator(data, rules))


class NotInRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': BLANK}
        rules = {'field': 'not_in:one,two,three'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': None}
        rules = {'field': 'not_in:one,two,three'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field': WHITE_SPACES}
        rules = {'field': 'not_in:one,two,three'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field': 'four'}
        rules = {'field': 'not_in:one,two,three'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field': '3'}
        rules = {'field': 'not_in:3.5,6,8,1,10e-2'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': '3'}
        rules = {'field': 'not_in:9,7,3,45'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': '56.5'}
        rules = {'field': ' not_in : 9 , 56.5 ,7 ,3,45 '}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field': 'two'}
        rules = {'field': 'not_in:one,two,three'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid4(self):
        data = {'field': 3}
        rules = {'field': 'not_in:3,6,8,1,10e-2'}
        self.assertFalse(build_validator(data, rules))


class BooleanRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field': BLANK}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field': None}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field': True}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field': False}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field': 0}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field': 1}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field': '0'}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field': '1'}
        rules = {'field': 'boolean'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field': '3'}
        rules = {'field': 'boolean'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field': '56.5'}
        rules = {'field': ' boolean '}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field': 'two'}
        rules = {'field': 'boolean'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid4(self):
        data = {'field': 3}
        rules = {'field': 'boolean'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid5(self):
        data = {'field': WHITE_SPACES}
        rules = {'field': 'boolean'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid6(self):
        data = {'field': 'True'}
        rules = {'field': 'boolean'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid7(self):
        data = {'field': 'False'}
        rules = {'field': 'boolean'}
        self.assertFalse(build_validator(data, rules))


class LessThanRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field1': 12, 'field2': 15}
        rules = {'field1': 'lt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field1': 16, 'field2': 15}
        rules = {'field2': 'lt:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field1': 'word', 'field2': 'word word'}
        rules = {'field1': 'lt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field1': 'word word', 'field2': 'word'}
        rules = {'field2': 'lt:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field1': (1, 2, 3, 4), 'field2': [1, 2, 3, 4, 5]}
        rules = {'field1': 'lt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field1': [1, 2, 3, 4, 5], 'field2': {1, 2, 3, 4}}
        rules = {'field2': 'lt:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field1': 12, 'field2': 12.5}
        rules = {'field1': 'lt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field1': 10e-4, 'field2': 10e-2}
        rules = {'field1': 'lt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid9(self):
        data = {'field1': BLANK, 'field2': WHITE_SPACES}
        rules = {'field1': 'lt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field1': 15, 'field2': 15}
        rules = {'field1': 'lt:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field1': 15, 'field2': 13}
        rules = {'field1': 'lt:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field1': 15.1, 'field2': 15}
        rules = {'field1': 'lt:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid4(self):
        data = {'field1': [1, 2, 3, 4, 5], 'field2': [1, 2, 3]}
        rules = {'field1': 'lt:field2'}
        self.assertFalse(build_validator(data, rules))

    # def test_invalid5(self):  # raises a ValueError exception
    #     data = {'field1': WHITE_SPACES, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'lt:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid6(self):  # raises a ValueError exception
    #     data = {'field1': None, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'lt:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid7(self):  # raises a ValueError exception
    #     data = {'field1': BLANK, 'field2': 20}
    #     rules = {'field1': 'lt:field2'}
    #     self.assertFalse(build_validator(data, rules))


class LessThanEqualRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field1': 12, 'field2': 15}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field1': 16, 'field2': 15}
        rules = {'field2': 'lte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field1': 'word', 'field2': 'word word'}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field1': 'word word', 'field2': 'word'}
        rules = {'field2': 'lte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field1': (1, 2, 3, 4), 'field2': [1, 2, 3, 4, 5]}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field1': [1, 2, 3, 4, 5], 'field2': {1, 2, 3, 4}}
        rules = {'field2': 'lte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field1': 12, 'field2': 12.5}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field1': 10e-4, 'field2': 10e-2}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid9(self):
        data = {'field1': BLANK, 'field2': WHITE_SPACES}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid10(self):
        data = {'field1': 'some word', 'field2': 'word word'}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid11(self):
        data = {'field1': 15, 'field2': 15}
        rules = {'field1': 'lte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid12(self):
        data = {'field1': [1, 2, 3, 4], 'field2': (1, 2, 3, 4)}
        rules = {'field2': 'lte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid1(self):
        data = {'field1': 15, 'field2': 13}
        rules = {'field1': 'lte:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field1': 15.1, 'field2': 15}
        rules = {'field1': 'lte:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field1': [1, 2, 3, 4, 5], 'field2': [1, 2, 3]}
        rules = {'field1': 'lte:field2'}
        self.assertFalse(build_validator(data, rules))

    # def test_invalid4(self):  # raises a ValueError exception
    #     data = {'field1': WHITE_SPACES, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'lte:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid5(self):  # raises a ValueError exception
    #     data = {'field1': None, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'lte:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid6(self):  # raises a ValueError exception
    #     data = {'field1': BLANK, 'field2': 20}
    #     rules = {'field1': 'lte:field2'}
    #     self.assertFalse(build_validator(data, rules))


class GreaterThanRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field1': 15, 'field2': 12}
        rules = {'field1': 'gt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field1': 15, 'field2': 16}
        rules = {'field2': 'gt:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field1': 'word word', 'field2': 'word'}
        rules = {'field1': 'gt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field1': 'word', 'field2': 'word word'}
        rules = {'field2': 'gt:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field1': [1, 2, 3, 4, 5], 'field2': (1, 2, 3, 4)}
        rules = {'field1': 'gt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field1': {1, 2, 3, 4}, 'field2': [1, 2, 3, 4, 5]}
        rules = {'field2': 'gt:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field1': 12.5, 'field2': 12}
        rules = {'field1': 'gt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field1': 10e-2, 'field2': 10e-4}
        rules = {'field1': 'gt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid9(self):
        data = {'field1': WHITE_SPACES, 'field2': BLANK}
        rules = {'field1': 'gt:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid(self):
        data = {'field1': 15, 'field2': 15}
        rules = {'field1': 'gt:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field1': 13, 'field2': 15}
        rules = {'field1': 'gt:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field1': 15, 'field2': 15.1}
        rules = {'field1': 'gt:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid4(self):
        data = {'field1': [1, 2, 3], 'field2': [1, 2, 3, 4, 5]}
        rules = {'field1': 'gt:field2'}
        self.assertFalse(build_validator(data, rules))

    # def test_invalid5(self):  # raises a ValueError exception
    #     data = {'field1': WHITE_SPACES, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'gt:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid6(self):  # raises a ValueError exception
    #     data = {'field1': None, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'gt:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid7(self):  # raises a ValueError exception
    #     data = {'field1': BLANK, 'field2': 20}
    #     rules = {'field1': 'gt:field2'}
    #     self.assertFalse(build_validator(data, rules))


class GreaterThanEqualRuleTest(unittest.TestCase):
    def test_valid(self):
        data = {'field1': 15, 'field2': 12}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid2(self):
        data = {'field1': 15, 'field2': 16}
        rules = {'field2': 'gte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid3(self):
        data = {'field1': 'word word', 'field2': 'word'}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid4(self):
        data = {'field1': 'word', 'field2': 'word word'}
        rules = {'field2': 'gte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid5(self):
        data = {'field1': [1, 2, 3, 4, 5], 'field2': (1, 2, 3, 4)}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid6(self):
        data = {'field1': {1, 2, 3, 4}, 'field2': [1, 2, 3, 4, 5]}
        rules = {'field2': 'gte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_valid7(self):
        data = {'field1': 12.5, 'field2': 12}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid8(self):
        data = {'field1': 10e-2, 'field2': 10e-4}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid9(self):
        data = {'field1': WHITE_SPACES, 'field2': BLANK}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid10(self):
        data = {'field1': 'word word', 'field2': 'some word'}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid11(self):
        data = {'field1': 15, 'field2': 15}
        rules = {'field1': 'gte:field2'}
        self.assertTrue(build_validator(data, rules))

    def test_valid12(self):
        data = {'field1': (1, 2, 3, 4), 'field2': [1, 2, 3, 4]}
        rules = {'field2': 'gte:field1'}
        self.assertTrue(build_validator(data, rules))

    def test_invalid1(self):
        data = {'field1': 13, 'field2': 1315}
        rules = {'field1': 'gte:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid2(self):
        data = {'field1': 15, 'field2': 15.1}
        rules = {'field1': 'gte:field2'}
        self.assertFalse(build_validator(data, rules))

    def test_invalid3(self):
        data = {'field1': [1, 2, 3], 'field2': [1, 2, 3, 4, 5]}
        rules = {'field1': 'gte:field2'}
        self.assertFalse(build_validator(data, rules))

    # def test_invalid4(self):  # raises a ValueError exception
    #     data = {'field1': WHITE_SPACES, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'gte:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid5(self):  # raises a ValueError exception
    #     data = {'field1': None, 'field2': [1, 2, 3]}
    #     rules = {'field1': 'gte:field2'}
    #     self.assertFalse(build_validator(data, rules))

    # def test_invalid6(self):  # raises a ValueError exception
    #     data = {'field1': BLANK, 'field2': 20}
    #     rules = {'field1': 'gte:field2'}
    #     self.assertFalse(build_validator(data, rules))


if __name__ == '__main__':
    unittest.main()
