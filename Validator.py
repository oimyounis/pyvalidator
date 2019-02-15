import re

class Validator:
    RULE_REQUIRED = 'required'
    RULE_EMAIL = 'email'
    RULE_NUMERIC = 'numeric'
    RULE_ENUM = 'enum'

    def __init__(self, data_dict, rules, messages={}):
        self.data = data_dict
        self.rules = rules
        self.messages = messages.copy()
        self._errors = {}
        self.fields = {}

        for fieldname in messages:
            msg = messages[fieldname]
            parts = fieldname.split('.')
            if parts[1] == self.RULE_REQUIRED:
                if parts[0] not in self.messages:
                    self.messages[parts[0]] = {}

                self.messages[parts[0]][self.RULE_REQUIRED] = msg
            elif parts[1] == self.RULE_EMAIL:
                if parts[0] not in self.messages:
                    self.messages[parts[0]] = {}

                self.messages[parts[0]][self.RULE_EMAIL] = msg
            elif parts[1] == self.RULE_NUMERIC:
                if parts[0] not in self.messages:
                    self.messages[parts[0]] = {}

                self.messages[parts[0]][self.RULE_NUMERIC] = msg
            elif parts[1] == self.RULE_ENUM:
                if parts[0] not in self.messages:
                    self.messages[parts[0]] = {}

                self.messages[parts[0]][self.RULE_ENUM] = msg

        for fieldname in rules:
            _rules = str(rules[fieldname])
            _rules = _rules.strip(' ')
            ruleparts = _rules.split(';')
            for rule in ruleparts:
                rule = rule.strip(' ')
                enumvalues = []

                if rule != '':
                    if rule.find(':') > -1:
                        enumparts = rule.split(':')
                        rule = enumparts[0]
                        enumvalues = enumparts[1].split(',')

                    if rule == self.RULE_REQUIRED:
                        message = None
                        if fieldname in self.messages and self.RULE_REQUIRED in self.messages[fieldname]:
                            message = self.messages[fieldname][self.RULE_REQUIRED]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        self.fields[fieldname].append(RequiredField(fieldname, value, message))
                    elif rule == self.RULE_EMAIL:
                        message = None
                        if fieldname in self.messages and self.RULE_EMAIL in self.messages[fieldname]:
                            message = self.messages[fieldname][self.RULE_EMAIL]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        self.fields[fieldname].append(EmailField(fieldname, value, message))
                    elif rule == self.RULE_NUMERIC:
                        message = None
                        if fieldname in self.messages and self.RULE_NUMERIC in self.messages[fieldname]:
                            message = self.messages[fieldname][self.RULE_NUMERIC]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        self.fields[fieldname].append(NumericField(fieldname, value, message))
                    elif rule == self.RULE_ENUM:
                        message = None
                        if fieldname in self.messages and self.RULE_ENUM in self.messages[fieldname]:
                            message = self.messages[fieldname][self.RULE_ENUM]

                        value = None
                        if fieldname in self.data:
                            value = self.data[fieldname]

                        if not fieldname in self.fields:
                            self.fields[fieldname] = []

                        enumfield = EnumField(fieldname, value, message)
                        enumfield.set_values(enumvalues)

                        self.fields[fieldname].append(enumfield)

    def valid(self):
        valid = True

        for fieldname in self.fields:
            fieldlist = self.fields[fieldname]
            for field in fieldlist:
                check = field.validate()
                if check is not True:
                    valid = False
                    if fieldname not in self._errors:
                        self._errors[fieldname] = []
                    self._errors[fieldname].append(check)

        return valid

    def errors(self, compact = False):
        if compact:
            msgs = []
            for f in self._errors:
                msglist = self._errors[f]
                for msg in msglist:
                    msgs.append(msg)

            return msgs
        else:
            return self._errors


class ValidationField:
    def __init__(self, fieldname, value, message = None):
        self.fieldname = fieldname
        self.value = value
        self.message = message
        classname = self.__class__.__name__.lower().replace('field', '')
        self.rule = classname

        if message != None:
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
        if self.value == '' or self.value == None:
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
        if not self.value or not re.match(r"^-?([1-9]+[0-9]*|([0-9]*\.[0-9]+))(e([1-9]+)|e-([1-9]+))?$", self.value):
            return self._invoke_error()
        return True


class EnumField(ValidationField):
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
        if not self.value:
            return self._invoke_error()

        found = False
        for val in self.Meta.values:
            if self.value == val:
                found = True
                break

        if found:
            return True

        return self._invoke_error()
