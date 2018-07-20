import datetime
from decimal import Decimal
from functools import wraps
import re
from six import string_types, integer_types

from .utils import float_to_decimal


def type_operator(priority_modifier=None):
    def wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            args = [self._validate_and_modify_value(arg, priority_modifier) for arg in args]
            kwargs = dict((k, self._validate_and_modify_value(v, priority_modifier))
                              for k, v in kwargs.items())
            return func(self, *args, **kwargs)
        return inner
    return wrapper


class BaseOperator(object):

    def __init__(self, value):
        self.value = self._validate_and_modify_value(value)

    def _validate_and_modify_value(self, value, priority_modifier=None):
        raise NotImplemented()


class StringOperator(BaseOperator):

    def _validate_and_modify_value(self, value, priority_modifier=None):
        value = value or ""
        if not isinstance(value, string_types):
            raise AssertionError("{0} is not a valid string type.".
                                 format(value))

        return priority_modifier(value) if callable(priority_modifier) else str(value)

    @type_operator(None)
    def same_as(self, target_string):
        return self.value == target_string

    @type_operator(None)
    def equal_to_case_insensitive(self, target_string):
        return self.value.lower() == target_string.lower()

    @type_operator(None)
    def starts_with(self, target_string):
        return self.value.startswith(target_string)

    @type_operator(None)
    def ends_with(self, target_string):
        return self.value.endswith(target_string)

    @type_operator(None)
    def contains(self, target_string):
        return target_string in self.value

    @type_operator(None)
    def matches_regex(self, regex):
        return re.search(regex, self.value)


class NumericOperator(BaseOperator):
    EPSILON = Decimal('0.000001')

    def get_modified_value(self, value, modifier, priority_modifier):
        return priority_modifier(value) if callable(priority_modifier) else modifier(value)

    def _validate_and_modify_value(self, value, priority_modifier=None):
        value = float(value)
        if isinstance(value, float):
            # In python 2.6, casting float to Decimal doesn't work
            return self.get_modified_value(value, float_to_decimal, priority_modifier)
        if isinstance(value, integer_types):
            return self.get_modified_value(value, Decimal, priority_modifier)
        if isinstance(value, Decimal):
            return self.get_modified_value(value, None, priority_modifier)
        else:
            raise AssertionError("{0} is not a valid numeric type.".
                                 format(value))

    @type_operator(None)
    def not_equal_to(self, target_number):
        return abs(self.value - target_number) > self.EPSILON

    @type_operator(None)
    def equal_to(self, target_number):
        return abs(self.value - target_number) <= self.EPSILON

    @type_operator(None)
    def greater_than(self, target_number):
        return (self.value - target_number) > self.EPSILON

    @type_operator(None)
    def greater_than_or_equal_to(self, target_number):
        return self.greater_than(target_number) or self.equal_to(target_number)

    @type_operator(None)
    def less_than(self, target_number):
        return (target_number - self.value) > self.EPSILON

    @type_operator(None)
    def less_than_or_equal_to(self, target_number):
        return self.less_than(target_number) or self.equal_to(target_number)


class DateTimeOperator(BaseOperator):

    def _validate_and_modify_value(self, value, priority_modifier=None):
        if not value:
            return
        try:
            return priority_modifier(value) if callable(priority_modifier) else \
                datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError, TypeError:
            raise AssertionError('{0} is not in valid date format'.format(value))
        except Exception as e:
            raise AssertionError('{0} exception {1}'.format(value, e.message))

    @type_operator(None)
    def is_before(self, target_moment):
        return self.value < target_moment

    @type_operator(None)
    def is_before_or_at(self, target_moment):
        return self.value <= target_moment

    @type_operator(None)
    def is_after(self, target_moment):
        return self.value > target_moment

    @type_operator(None)
    def is_after_or_at(self, target_moment):
        return self.value >= target_moment

    @type_operator(None)
    def is_at(self, target_moment):
        return self.value == target_moment

    @type_operator(None)
    def is_not_at(self, target_moment):
        return self.value != target_moment

    @type_operator(lambda moment_map: datetime.timedelta(**moment_map))
    def is_at_moments_before_now(self, target_moment):
        return datetime.datetime.now() - self.value == target_moment

    @type_operator(None)
    def is_not_in_future(self, dummy):
        return self.value < datetime.datetime.now()
