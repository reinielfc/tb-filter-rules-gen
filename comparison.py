from enum import Enum

class Comparison:
	def __init__(self, property: str, operator: str, criteria: str) -> "Comparison":
		self._property = property
		self._operator = operator
		self._criteria = criteria

	def __str__(self) -> str:
		return "(" + ",".join([self._property, self._operator, str(self._criteria) or ""]) + ")"


class ComparisonOperator(Enum):
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
		return lambda *criteria: [self.comparing(property, c) for c in criteria]


class StatusComparison:
	def __init__(self, property: str):
		self.isequalto = ComparisonOperator.IS_EQUAL_TO.using(property)
		self.isnotequalto = ComparisonOperator.IS_NOT_EQUAL_TO.using(property)


class BigStringComparison(StatusComparison):
	def __init__(self, property: str):
		super().__init__(property)
		self.contains = ComparisonOperator.CONTAINS.using(property)
		self.doesnotcontain = ComparisonOperator.DOES_NOT_CONTAIN.using(property)


class StringComparison(BigStringComparison):
	def __init__(self, property: str):
		super().__init__(property)
		self.beginswith = ComparisonOperator.BEGINS_WITH.using(property)
		self.endswith = ComparisonOperator.ENDS_WITH.using(property)


class AddressComparison(StringComparison):
	def __init__(self, property: str):
		super().__init__(property)
		self.isinab = ComparisonOperator.IS_IN_AB.using(property)
		self.isnotinab = ComparisonOperator.IS_NOT_IN_AB.using(property)


class DateComparison(StatusComparison):
	def __init__(self, property: str):
		super().__init__(property)
		self.isbefore = ComparisonOperator.IS_BEFORE.using(property)
		self.isafter = ComparisonOperator.IS_AFTER.using(property)


class PriorityComparison(StatusComparison):
	def __init__(self, property: str):
		super().__init__(property)
		self.ishigherthan = ComparisonOperator.IS_HIGHER_THAN.using(property)
		self.islowerthan = ComparisonOperator.IS_LOWER_THAN.using(property)


class AgeInDaysComparison:
	def __init__(self, property: str) -> None:
		self.isequalto = ComparisonOperator.IS_EQUAL_TO.using(property)
		self.islessthan = ComparisonOperator.IS_LESS_THAN.using(property)
		self.isgreaterthan = ComparisonOperator.IS_GREATER_THAN.using(property)


class TagComparison(BigStringComparison):
	def __init__(self, property: str):
		super().__init__(property)
		self.isempty = ComparisonOperator.IS_EMPTY.using(property)
		self.isnotempty = ComparisonOperator.IS_NOT_EMPTY.using(property)


class ExpressionSearchStringComparison:
	def __init__(self, property: str) -> None:
		self.contains = ComparisonOperator.CONTAINS.using(f"expressionsearch#{property}")
		self.doesnotcontain = ComparisonOperator.DOES_NOT_CONTAIN.using(f"expressionsearch#{property}")


class ExpressionSearchDateComparison:
	def __init__(self, property: str):
		self.isbefore = ComparisonOperator.IS_BEFORE.using(f"expressionsearch#{property}")
		self.isafter = ComparisonOperator.IS_AFTER.using(f"expressionsearch#{property}")


class ExpressionSearchMatch:
	def __init__(self, property: str):
		self.matches = ComparisonOperator.MATCHES.using(f"expressionsearch#{property}")
		self.doesnotmatch = ComparisonOperator.DOES_NOT_MATCH.using(f"expressionsearch#{property}")


class ExpressionSearch:
	bcc = ExpressionSearchStringComparison("Bcc")
	tosomebodyonly = ExpressionSearchStringComparison("toSomebodyOnly")
	subjectsimple = ExpressionSearchStringComparison("subjectSimple")
	datematch = ExpressionSearchStringComparison("dateMatch")
	attachmentnameortype = ExpressionSearchStringComparison("attachmentNameOrType")
	xnote = ExpressionSearchStringComparison("XNote")

	daytime = ExpressionSearchDateComparison("dayTime")

	subjectregex = ExpressionSearchMatch("subjectRegex")
	headerregex = ExpressionSearchMatch("headerRegex")
	senderregex = ExpressionSearchMatch("fromRegex")
	receiverregex = ExpressionSearchMatch("toRegex")
	bodyregex = ExpressionSearchMatch("bodyRegex")

class ComparisonListBuilder:
	subject = StringComparison("subject")

	# address
	sender = AddressComparison("from")
	receiver = AddressComparison("to")
	cc = AddressComparison("cc")
	receiverorcc = AddressComparison("to or cc")
	alladdresses = AddressComparison("all addresses")

	body = BigStringComparison("body")
	date = DateComparison("date")
	priority = PriorityComparison("priority")
	status = StatusComparison("status")
	ageindays = AgeInDaysComparison("age in days")
	tag = TagComparison("tag")

	expressionsearch = ExpressionSearch