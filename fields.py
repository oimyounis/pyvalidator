import re
from helpers import is_str, is_numeric, is_iterable


class ValidationField:
    def __init__(self, fieldname, value, message=None, _validator=None):
        self.fieldname = fieldname
        self.value = value
        self.message = message
        classname = self.__class__.__name__.lower().replace('field', '')
        self.rule = classname
        self._validator = _validator

        if message is not None:
            self.message = message
        else:
            self.construct_message()
            pass

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            self.message = self.Meta.message.replace('{#fieldname#}', self.fieldname)

    def _invoke_error(self):
        return self.message

    def validate(self):
        pass


class RequiredField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} is required'

    def validate(self):
        if self.value == '' or self.value is None or isinstance(self.value, (list, tuple, set)) and not self.value:
            return self._invoke_error()
        return True


class EmailField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} is not a valid email address'

    def validate(self):
        if self.value and not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.value):
            return self._invoke_error()
        return True


class NumericField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} accepts numbers only'

    def validate(self):
        if self.value and not re.match(r"^-?([1-9]+[0-9]*|([0-9]*\.[0-9]+))(e([1-9]+)|e\+([1-9]+)|e-([1-9]+))?$", str(self.value))\
                or self.value and not isinstance(self.value, (str, int, float)):
            return self._invoke_error()
        return True


class InField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} accepts only these values: {#values#}'
        values = []

    def set_values(self, values):
        self.Meta.values = values
        self.construct_message()

    def get_values(self):
        return self.Meta.values

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(InField, self).construct_message()
            self.message = self.message.replace('{#values#}', ', '.join(self.get_values()))

    def validate(self):
        if str(self.value) in self.get_values() or self.value == '' or self.value is None:
            return True

        return self._invoke_error()


class MaxField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} has a maximum of: {#value#}'
        value = None

    def set_value(self, value):
        isstr = isinstance(value, str)
        isfloating = isstr and value.find('.') > -1

        if isstr:
            try:
                value = float(value) if isfloating else int(value)
            except ValueError:
                raise ValueError('Value supplied to the "max" rule must be of type int or float')

        self.Meta.value = value
        self.construct_message()

    def get_value(self):
        return self.Meta.value

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(MaxField, self).construct_message()
            self.message = self.message.replace('{#value#}', str(self.get_value()))

    def validate(self):
        if self.value is None:
            return True

        if isinstance(self.value, (str, list, tuple, set)):
            if len(self.value) <= self.get_value():
                return True
        elif isinstance(self.value, (int, float)):
            if self.value <= self.get_value():
                return True

        return self._invoke_error()


class MinField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} has a minimum of: {#value#}'
        value = None

    def set_value(self, value):
        isstr = isinstance(value, str)
        isfloating = isstr and value.find('.') > -1

        if isstr:
            try:
                value = float(value) if isfloating else int(value)
            except ValueError:
                raise ValueError('Value supplied to the "min" rule must be of type int or float')

        self.Meta.value = value
        self.construct_message()

    def get_value(self):
        return self.Meta.value

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(MinField, self).construct_message()
            self.message = self.message.replace('{#value#}', str(self.get_value()))

    def validate(self):
        if self.value is None:
            return True

        if isinstance(self.value, (str, list, tuple, set)):
            if len(self.value) >= self.get_value():
                return True
        elif isinstance(self.value, (int, float)):
            if self.value >= self.get_value():
                return True

        return self._invoke_error()


class NotInField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} must not be one of these values: {#values#}'
        values = []

    def set_values(self, values):
        self.Meta.values = values
        self.construct_message()

    def get_values(self):
        return self.Meta.values

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(NotInField, self).construct_message()
            self.message = self.message.replace('{#values#}', ', '.join(self.get_values()))

    def validate(self):
        if str(self.value) not in self.get_values() or self.value == '' or self.value is None:
            return True

        return self._invoke_error()


class BooleanField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} must be one of these values: True, False, 0, 1, "0" or "1"'

    def validate(self):
        if self.value in (True, False, 0, 1, '0', '1', '', None):
            return True

        return self._invoke_error()


class LessThanField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} must be less than the field {#otherfieldname#} in size'
        value = None

    def set_value(self, value):
        self.Meta.value = value
        self.construct_message()

    def get_value(self):
        return self.Meta.value

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(LessThanField, self).construct_message()
            self.message = self.message.replace('{#otherfieldname#}', str(self.get_value()))

    def validate(self):
        othervalue = self._validator.data[self.get_value()]

        if is_iterable(self.value) and not is_iterable(othervalue) \
            or is_numeric(self.value) and not is_numeric(othervalue) \
                or not is_iterable(self.value) and not is_numeric(self.value) and type(self.value) != type(othervalue):
            raise ValueError('The two values in a "less than" comparison must be of the same type. Found %s and %s.' %
                             (self.value.__class__.__name__, othervalue.__class__.__name__))

        if is_str(self.value) or is_iterable(self.value):
            if len(self.value) < len(othervalue):
                return True
        elif is_numeric(self.value):
            if self.value < othervalue:
                return True

        return self._invoke_error()


class LessThanEqualField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} must be less than or equal to the field {#otherfieldname#} in size'
        value = None

    def set_value(self, value):
        self.Meta.value = value
        self.construct_message()

    def get_value(self):
        return self.Meta.value

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(LessThanEqualField, self).construct_message()
            self.message = self.message.replace('{#otherfieldname#}', str(self.get_value()))

    def validate(self):
        othervalue = self._validator.data[self.get_value()]

        if is_iterable(self.value) and not is_iterable(othervalue) \
            or is_numeric(self.value) and not is_numeric(othervalue) \
                or not is_iterable(self.value) and not is_numeric(self.value) and type(self.value) != type(othervalue):
            raise ValueError('The two values in a "less than or equal" comparison must be of the same type. Found %s and %s.' %
                             (self.value.__class__.__name__, othervalue.__class__.__name__))

        if is_str(self.value) or is_iterable(self.value):
            if len(self.value) <= len(othervalue):
                return True
        elif is_numeric(self.value):
            if self.value <= othervalue:
                return True

        return self._invoke_error()


class GreaterThanField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} must be greater than the field {#otherfieldname#} in size'
        value = None

    def set_value(self, value):
        self.Meta.value = value
        self.construct_message()

    def get_value(self):
        return self.Meta.value

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(GreaterThanField, self).construct_message()
            self.message = self.message.replace('{#otherfieldname#}', str(self.get_value()))

    def validate(self):
        othervalue = self._validator.data[self.get_value()]

        if is_iterable(self.value) and not is_iterable(othervalue) \
            or is_numeric(self.value) and not is_numeric(othervalue) \
                or not is_iterable(self.value) and not is_numeric(self.value) and type(self.value) != type(othervalue):
            raise ValueError('The two values in a "greater than" comparison must be of the same type. Found %s and %s.' %
                             (self.value.__class__.__name__, othervalue.__class__.__name__))

        if is_str(self.value) or is_iterable(self.value):
            if len(self.value) > len(othervalue):
                return True
        elif is_numeric(self.value):
            if self.value > othervalue:
                return True

        return self._invoke_error()


class GreaterThanEqualField(ValidationField):
    class Meta:
        message = 'Field {#fieldname#} must be greater than or equal to the field {#otherfieldname#} in size'
        value = None

    def set_value(self, value):
        self.Meta.value = value
        self.construct_message()

    def get_value(self):
        return self.Meta.value

    def construct_message(self):
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'message'):
            super(GreaterThanEqualField, self).construct_message()
            self.message = self.message.replace('{#otherfieldname#}', str(self.get_value()))

    def validate(self):
        othervalue = self._validator.data[self.get_value()]

        if is_iterable(self.value) and not is_iterable(othervalue) \
            or is_numeric(self.value) and not is_numeric(othervalue) \
                or not is_iterable(self.value) and not is_numeric(self.value) and type(self.value) != type(othervalue):
            raise ValueError('The two values in a "greater than or equal" comparison must be of the same type. Found %s and %s.' %
                             (self.value.__class__.__name__, othervalue.__class__.__name__))

        if is_str(self.value) or is_iterable(self.value):
            if len(self.value) >= len(othervalue):
                return True
        elif is_numeric(self.value):
            if self.value >= othervalue:
                return True

        return self._invoke_error()
