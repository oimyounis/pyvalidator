import re


class Validator:
    RULE_REQUIRED = 'required'
    RULE_EMAIL = 'email'
    RULE_NUMERIC = 'numeric'
    RULE_IN = 'in'
    RULE_MAX = 'max'
    RULE_MIN = 'min'
    RULE_NOT_IN = 'not_in'

    def __init__(self, data_dict, rules, messages={}):
        self.data = data_dict
        self.rules = rules
        self.messages = messages.copy()
        self._errors = {}
        self.fields = {}

        for fieldname, msg in messages.items():
            parts = fieldname.split('.')
            field = parts[0]
            rule = parts[1]

            if field not in self.messages:
                self.messages[field] = {}

            self.messages[field][rule] = msg

        for fieldname, _rules in rules.items():
            _rules = str(_rules).strip()
            ruleparts = _rules.split('|')
            for rule in ruleparts:
                rule = rule.strip()
                rulevalue = ''

                if rule:
                    if rule.find(':') > -1:
                        ruleparts = rule.split(':')
                        rule = ruleparts[0].strip()
                        rulevalue = ruleparts[1].strip()

                    if rule == Validator.RULE_REQUIRED:
                        message = None
                        if fieldname in self.messages and Validator.RULE_REQUIRED in self.messages[fieldname]:
                            message = self.messages[fieldname][Validator.RULE_REQUIRED]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        self.fields[fieldname].append(RequiredField(fieldname, value, message))
                    elif rule == Validator.RULE_EMAIL:
                        message = None
                        if fieldname in self.messages and Validator.RULE_EMAIL in self.messages[fieldname]:
                            message = self.messages[fieldname][Validator.RULE_EMAIL]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        self.fields[fieldname].append(EmailField(fieldname, value, message))
                    elif rule == Validator.RULE_NUMERIC:
                        message = None
                        if fieldname in self.messages and Validator.RULE_NUMERIC in self.messages[fieldname]:
                            message = self.messages[fieldname][Validator.RULE_NUMERIC]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        self.fields[fieldname].append(NumericField(fieldname, value, message))
                    elif rule == Validator.RULE_IN:
                        enumvalues = rulevalue.replace(' ', '').split(',')

                        message = None
                        if fieldname in self.messages and Validator.RULE_IN in self.messages[fieldname]:
                            message = self.messages[fieldname][Validator.RULE_IN]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        enumfield = InField(fieldname, value, message)
                        enumfield.set_values(enumvalues)

                        self.fields[fieldname].append(enumfield)
                    elif rule == Validator.RULE_MAX:
                        message = None
                        if fieldname in self.messages and Validator.RULE_MAX in self.messages[fieldname]:
                            message = self.messages[fieldname][Validator.RULE_MAX]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        maxfield = MaxField(fieldname, value, message)
                        maxfield.set_value(rulevalue)

                        self.fields[fieldname].append(maxfield)
                    elif rule == Validator.RULE_MIN:
                        message = None
                        if fieldname in self.messages and Validator.RULE_MIN in self.messages[fieldname]:
                            message = self.messages[fieldname][Validator.RULE_MIN]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        minfield = MinField(fieldname, value, message)
                        minfield.set_value(rulevalue)

                        self.fields[fieldname].append(minfield)
                    elif rule == Validator.RULE_NOT_IN:
                        enumvalues = rulevalue.replace(' ', '').split(',')

                        message = None
                        if fieldname in self.messages and Validator.RULE_NOT_IN in self.messages[fieldname]:
                            message = self.messages[fieldname][Validator.RULE_NOT_IN]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        enumfield = NotInField(fieldname, value, message)
                        enumfield.set_values(enumvalues)

                        self.fields[fieldname].append(enumfield)

    def valid(self):
        valid = True

        for fieldname, fieldlist in self.fields.items():
            for field in fieldlist:
                check = field.validate()
                if check is not True:
                    valid = False
                    if fieldname not in self._errors:
                        self._errors[fieldname] = []
                    self._errors[fieldname].append(check)

        return valid

    def errors(self, compact=False):
        if compact:
            msgs = []
            for msglist in self._errors.values():
                for msg in msglist:
                    msgs.append(msg)

            return msgs
        else:
            return self._errors


class ValidationField:
    def __init__(self, fieldname, value, message=None):
        self.fieldname = fieldname
        self.value = value
        self.message = message
        classname = self.__class__.__name__.lower().replace('field', '')
        self.rule = classname

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
            self.message = self.Meta.message.replace('{#fieldname#}', self.fieldname)
            self.message = self.message.replace('{#values#}', ', '.join(self.Meta.values))

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
            self.message = self.message.replace('{#value#}', str(self.Meta.value))

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
            self.message = self.message.replace('{#value#}', str(self.Meta.value))

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
            self.message = self.Meta.message.replace('{#fieldname#}', self.fieldname)
            self.message = self.message.replace('{#values#}', ', '.join(self.Meta.values))

    def validate(self):
        if str(self.value) not in self.get_values() or self.value == '' or self.value is None:
            return True

        return self._invoke_error()


def prepare_validation_errors(errors, compact=False):
    errors_dict = {}
    errors_arr = []

    for err_arr in errors:
        errs = []

        for err in err_arr[1]:
            errs.append(err)
            errors_arr.append(err)

        errors_dict[err_arr[0]] = errs

    if compact:
        return errors_arr

    return errors_dict
