from enum import Enum
from .comparison import Comparison


class ConditionOperator(Enum):
	OR = "OR"
	AND = "AND"

	def __str__(self):
		return self.value


class ConditionList:
	def __init__(self, operator: ConditionOperator) -> None:
		self._operator = operator
		self._comparisons: list[Comparison] = []

	def append(self, comparisonlist: list[Comparison] = [], comparison: Comparison = None):
		if comparison != None:
			comparisonlist.append(comparison)

		for c in comparisonlist:
			self._comparisons.append(c)

		return self

	def __str__(self) -> str:
		return f"{self._operator} " + f" {self._operator} ".join([str(c) for c in self._comparisons])
