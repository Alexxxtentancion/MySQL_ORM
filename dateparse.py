import re
import datetime

date_re = re.compile(
    r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$'
)


# Support the sections of ISO 8601 date representation that are accepted by
# timedelta


def parse_date(value):
    match = date_re.match(value)
    if match:
        kw = {k: int(v) for k, v in match.groupdict().items()}
        return datetime.datetime(**kw)

print(type(parse_date('1992-12-12')))