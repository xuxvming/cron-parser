import unittest
from cron_parser import CronParser


class ParserTest(unittest.TestCase):

    def test_parser(self):
        s = '*/15 0 1,15 * 1-5 /user/bin/'
        parser = CronParser(s)
        res = parser.translate()
        print(res)
        expected = dict(minute=[0, 15, 30, 45],
                        hour=[0],
                        day=[1, 15], month=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], week=[1, 2, 3, 4, 5],
                        command='/user/bin/')

        self.assertDictEqual(expected, res)

    def test_with_bad_expression(self):
        s = '*/15 0 * * 1- /user/bin'
        parser = CronParser(s)
        self.assertRaises(ValueError, parser.translate)

    def test_with_string_value(self):
        s = '*/15 0 * * SUN /user/bin'
        parse = CronParser(s)
        res = parse.translate()
        expected = dict(minute=[0, 15, 30, 45], hour=[0],
                        day=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                              26, 27, 28, 29, 30, 31], month=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], week=[7],
                        command='/user/bin')
        self.assertDictEqual(expected, res)

    def test_with_incorrect_expression(self):
        s = '*/15 0 JAN * SUN /user/bin'
        parser = CronParser(s)
        self.assertRaises(ValueError, parser.translate)

    def test_with_increase_bigger_than_upper_limit(self):
        s = '*/80 0 * * SUN /user/bin'
        parser = CronParser(s)
        self.assertRaises(AssertionError, parser.translate)
