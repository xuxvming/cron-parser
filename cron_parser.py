import log_module
import re

logger = log_module.setup_custom_logger(__name__)


def parse_all(entity, upper_limit, step, separation):
    start = 1
    if entity == 'minute' or entity == 'hour':
        start = 0

    if separation == '/':
        res = [i for i in range(start, upper_limit, step)]
    else:
        if separation == ',' or separation == '-':
            logger.warning('No value detected after [{}], treat this as *'.format(separation))
        res = [i for i in range(start, upper_limit)]
    return res


def parse_each(start, step, upper_limit, separation):
    if separation == '/':
        res = [i for i in range(start, upper_limit, step)]
    elif separation == ',':
        res = [start, step]
    elif separation == '-':
        res = [i for i in range(start, step + 1)]
    else:
        res = [start]
    return res


def to_file(res):
    text_file = open('out.txt', 'w')
    logger.info('Output to file out.txt')
    for key in res:
        if isinstance(res[key], list):
            line = ' '.join([str(i) for i in res[key]])
        else:
            line = res[key]
        text_file.write(str(key) + ' {}\n'.format(line))
    text_file.close()


def get_upper_limit(index):
    if index == 0:
        return 60, 'minute'
    if index == 1:
        return 24, 'hour'
    elif index == 2:
        return 32, 'day'
    elif index == 3:
        return 13, 'month'
    else:
        return 8, 'week'


def pretty_print(res):
    for key in res:
        if isinstance(res[key], list):
            line = ' '.join([str(i) for i in res[key]])
        else:
            line = res[key]
        print(str(key) + ' {}\n'.format(line))


class CronParser:

    def __init__(self, cron_expression):
        self.cron_expression = cron_expression
        logger.info('Parsing expression: [{}]'.format(cron_expression))
        self.month_date_dict = {
            'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8,
            'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12,
            'MON': 1, 'TUE': 2, 'WED': 3, 'THU': 4, 'FRI': 5, 'SAT': 6, 'SUN': 7
        }

    def translate(self):
        res = dict()
        expression_string = self.cron_expression.split(' ')
        for i in range(0, len(expression_string) - 1):
            temp = self.parse(expression_string[i], i)
            res.update(temp)
        res.update({'command': expression_string[-1]})
        to_file(res)
        return res

    def parse(self, expression, i):
        matcher = re.match('(\*|\d+|[A-Z]{3})(\/|\,|-)?(\d+)?', expression)
        upper_limit, entity = get_upper_limit(i)
        if matcher:
            start, separation, step = self.validate_expression(matcher, i)
            if step >= upper_limit:
                raise AssertionError('Change step cannot exceed upper limit')
            if start == '*':
                res = parse_all(entity, upper_limit, step, separation)
            else:
                res = parse_each(start, step, upper_limit, separation)
        else:
            raise ValueError('Invalid cron expression {}'.format(expression))
        return {entity: res}

    def validate_expression(self, matcher, index):
        separation = ''
        step = 1

        if matcher.group(1) in self.month_date_dict:
            start = self.month_date_dict[matcher.group(1)]
            if not (index == 3 or index == 4):
                raise ValueError('Incorrect usage detected !')
        elif matcher.group(1) == '*':
            start = '*'
        else:
            start = int(matcher.group(1))

        if matcher.group(2):
            separation = matcher.group(2)
            if matcher.group(3) is None:
                raise ValueError('Missing value after {}'.format(separation))
            else:
                step = int(matcher.group(3))
        return start, separation, step
