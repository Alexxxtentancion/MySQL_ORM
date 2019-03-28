from dateparse import parse_date
import datetime
from exceptions import DoesNotExist, MultyplyObjectReturn, ValidationError,InputError


class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.default = default

    def validate(self, value):
        if value is None and not self.required:
            return None
        elif value is None and self.required:
            raise InputError('Need to input requierd fields in {}s'.format(type(self).__name__))
        if self.f_type == datetime.date:
            if isinstance(value, datetime.date):
                return value.strftime('%Y-%m-%d')
            elif isinstance(value, list) or isinstance(value, tuple):
                return datetime.date(*value).strftime('%Y-%m-%d')
            elif isinstance(value, dict):
                return datetime.date(**value).strftime('%Y-%m-%d')
            elif isinstance(value,str):
                try:
                    parsed = parse_date(value)
                    if parsed is not None:
                        return parsed.strftime('%Y-%m-%d')
                except ValueError:
                    raise ValidationError('invalid_date',
                                          code='invalid_date',
                                          params={'value': value},

                                          )


        return self.f_type(value)


class IntField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(int, required, default)


class StringField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(str, required, default)


class DateField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(datetime.date, required, default)