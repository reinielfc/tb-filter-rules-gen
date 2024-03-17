from enum import Enum
from .action import Action
from .condition import ConditionOperator, ConditionList
from .comparison import Comparison
from .rules import Rules


class Enabled(Enum):
	YES = "yes"
	NO = "no"

	def __str__(self) -> str:
		return self.value


class FilterType(Enum):
	MANUALLY_RUN = 16
	GETTING_NEW_MAIL__FILTER_BEFORE_JUNK_CLASSIFICATION = 1
	GETTING_NEW_MAIL__FILTER_AFTER_JUNK_CLASSIFICATION = 32
	ARCHVIVING = 128
	AFTER_SAVING = 64
	PERIODICALLY_EVERY_10_MINUTES = 256

	# add types up to mix and match (33 is not available)
	DEFAULT = MANUALLY_RUN + GETTING_NEW_MAIL__FILTER_BEFORE_JUNK_CLASSIFICATION

	def __str__(self) -> str:
		return str(self.value)


class Filter(Rules):
	def __init__(self, name, type = FilterType.DEFAULT, enabled = Enabled.YES, operator = ConditionOperator.OR) -> 'Filter':
		self._name = name
		self._enabled = enabled
		self._type = type
		self._condition = ConditionList(operator)
		self._actions: list[Action] = []

	def do(self, action: Action):
		self._actions.append(action)
		return self

	def when(self, comparison: list[Comparison]) -> 'Filter':
		self._condition.append(comparison)
		return self
	
	def rules(self) -> list[str]:
		return [
			self.rulestr(name=self._name),
			self.rulestr(enabled=self._enabled),
			self.rulestr(type=self._type),
			*[rules for action in self._actions for rules in action.rules()],
			self.rulestr(condition=self._condition)
		]


class FilterList(Rules):
	def __init__(self, *filter: Filter, version = 9, logging = Enabled.YES) -> None:
		self._version = version
		self._logging = logging
		self._filters = list(filter)

	def rules(self) -> list[str]:
		return [
			self.rulestr(version=self._version),
			self.rulestr(logging=self._logging),
			*[rule for filter in self._filters for rule in filter.rules()]
		]
	
	def display(self):
		print(self)
