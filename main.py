import cron_parser as parser
from cron_parser import pretty_print
import sys

if __name__ == '__main__':
    cron_expression = str(sys.argv[1])
    parser = parser.CronParser(cron_expression)
    res = parser.translate()
    pretty_print(res)
