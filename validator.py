from fields import *


class Validator:
    RULE_REQUIRED = 'required'
    RULE_EMAIL = 'email'
    RULE_NUMERIC = 'numeric'
    RULE_IN = 'in'
    RULE_MAX = 'max'
    RULE_MIN = 'min'
    RULE_NOT_IN = 'not_in'
    RULE_BOOLEAN = 'boolean'
    RULE_LT = 'lt'

    @classmethod
    def _is_valid_rule(cls, rule):
        return hasattr(cls, 'RULE_%s' % rule.upper())

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

                    if not Validator._is_valid_rule(rule):
                        continue

                    message = None
                    if fieldname in self.messages and rule in self.messages[fieldname]:
                        message = self.messages[fieldname][rule]

                    value = None
                    if fieldname in self.data:
                        value = self.data[fieldname]

                    if fieldname not in self.fields:
                        self.fields[fieldname] = []

                    if rule == Validator.RULE_REQUIRED:
                        self.fields[fieldname].append(RequiredField(fieldname, value, message))
                    elif rule == Validator.RULE_EMAIL:
                        self.fields[fieldname].append(EmailField(fieldname, value, message))
                    elif rule == Validator.RULE_NUMERIC:
                        self.fields[fieldname].append(NumericField(fieldname, value, message))
                    elif rule == Validator.RULE_IN:
                        enumvalues = rulevalue.replace(' ', '').split(',')

                        enumfield = InField(fieldname, value, message)
                        enumfield.set_values(enumvalues)

                        self.fields[fieldname].append(enumfield)
                    elif rule == Validator.RULE_MAX:
                        maxfield = MaxField(fieldname, value, message)
                        maxfield.set_value(rulevalue)

                        self.fields[fieldname].append(maxfield)
                    elif rule == Validator.RULE_MIN:
                        minfield = MinField(fieldname, value, message)
                        minfield.set_value(rulevalue)

                        self.fields[fieldname].append(minfield)
                    elif rule == Validator.RULE_NOT_IN:
                        enumvalues = rulevalue.replace(' ', '').split(',')

                        enumfield = NotInField(fieldname, value, message)
                        enumfield.set_values(enumvalues)

                        self.fields[fieldname].append(enumfield)
                    elif rule == Validator.RULE_BOOLEAN:
                        self.fields[fieldname].append(BooleanField(fieldname, value, message))
                    elif rule == Validator.RULE_LT:
                        lessthanfield = LessThanField(fieldname, value, message, self)
                        lessthanfield.set_value(rulevalue)

                        self.fields[fieldname].append(lessthanfield)

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
