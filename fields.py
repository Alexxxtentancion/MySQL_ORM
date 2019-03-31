import datetime

from exceptions import *


class Field:
    def __init__(self, f_type, required=True, default=None):
        self.f_type = f_type
        self.required = required
        self.default = default

    def validate(self, value):
        if value is None and not self.required:
            return None
        elif value is None and self.required:
            raise InputError('Need to input required fields in {}s'.format(type(self).__name__))
        if self.f_type == datetime.date:
            if isinstance(value, datetime.date):
                return value.strftime('%Y-%m-%d')
            elif isinstance(value, list) or isinstance(value, tuple):
                return datetime.date(*value).strftime('%Y-%m-%d')
            elif isinstance(value, dict):
                return datetime.date(**value).strftime('%Y-%m-%d')
            elif isinstance(value, str):
                return datetime.datetime.strptime(value, '%Y-%m-%d').strftime('%Y-%m-%d')
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


class FloatField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(float, required, default)


class BooleanField(Field):
    def __init__(self, required=False, default=None):
        super().__init__(bool, required, default)
