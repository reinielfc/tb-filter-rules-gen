from enum import Enum


class Comparison:
    def __init__(self, property: str, operator: str, criteria: str) -> "Comparison":
        self.property: str = property
        self.operator: str = operator
        self.criteria: str = criteria

    def __str__(self) -> str:
        return ",".join([self.property, self.operator, self.criteria or ""])


class Operator(Enum):
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "doesn't contain"

    IS_EQUAL_TO = "is"
    IS_NOT_EQUAL_TO = "isn't"

    BEGINS_WITH = "begins with"
    ENDS_WITH = "ends with"

    IS_IN_AB = "is in ab"
    IS_NOT_IN_AB = "isn't in ab"

    IS_BEFORE = "is before"
    IS_AFTER = "is after"

    IS_HIGHER_THAN = "is higher than"
    IS_LOWER_THAN = "is lower than"

    IS_LESS_THAN = "is less than"
    IS_GREATER_THAN = "is greater than"

    IS_EMPTY = "is empty"
    IS_NOT_EMPTY = "isn't empty"

    MATCHES = "matches"
    DOES_NOT_MATCH = "doesn't match"

    def __new__(cls, value: str):
        new_operator = object.__new__(cls)
        new_operator._value_ = value
        new_operator.comparing = lambda p, c: Comparison(p, value, c)
        return new_operator

    def using(self, property: str):
        return lambda criteria = None: self.comparing(property, criteria)


class StatusComparison:
    def __init__(self, property: str):
        self.isequalto = Operator.IS_EQUAL_TO.using(property)
        self.isnotequalto = Operator.IS_NOT_EQUAL_TO.using(property)


class BigStringComparison(StatusComparison):
    def __init__(self, property: str):
        super().__init__(property)
        self.contains = Operator.CONTAINS.using(property)
        self.doesnotcontain = Operator.DOES_NOT_CONTAIN.using(property)


class StringComparison(BigStringComparison):
    def __init__(self, property: str):
        super().__init__(property)
        self.beginswith = Operator.BEGINS_WITH.using(property)
        self.endswith = Operator.ENDS_WITH.using(property)


class AddressComparison(StringComparison):
    def __init__(self, property: str):
        super().__init__(property)
        self.isinab = Operator.IS_IN_AB.using(property)
        self.isnotinab = Operator.IS_NOT_IN_AB.using(property)


class TagComparison(BigStringComparison):
    def __init__(self, property: str):
        super().__init__(property)
        self.isempty = Operator.IS_EMPTY.using(property)
        self.isnotempty = Operator.IS_NOT_EMPTY.using(property)


class Comparing:
    subject = StringComparison("subject")

    sender = AddressComparison("from")
    receiver = AddressComparison("to")
    cc = AddressComparison("cc")
    receiver_or_cc = AddressComparison("to or cc")
    all_addresses = AddressComparison("all addresses")

    body = BigStringComparison("body")

    # ...

    status = StatusComparison("status")
    tag = TagComparison("tag")


print(Comparing.tag.isempty())  # -> subject,begins with,test
