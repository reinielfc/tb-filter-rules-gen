
import re
from typing import OrderedDict


class Comparison:
    def __init__(self, header: str, comparator: str, string: str):
        self.header = header
        self.comparator = comparator
        self.string = string

    def __hash__(self) -> int:
        return hash(self.header) ^ hash(self.comparator) ^ hash(self.string)

    def __eq__(self, other) -> bool:
        return self.string == other.string \
            and self.header == other.header \
            and self.comparator == other.comparator

    def __str__(self) -> str:
        return f'({self.header},{self.comparator},{self.string})'


class Condition:
    def __init__(self, comparisons: set[Comparison] = None, mode: str = 'OR'):
        self.mode = mode
        self.comparisons: set[Comparison] = comparisons or set()

    def __str__(self):
        return ' '.join([
            f'{self.mode} {comparison}'
            for comparison in self.comparisons])

    def sortComparisons(self):
        comparisons: set[Comparison] = self.comparisons
        self.comparisons = sorted(
            comparisons, key=lambda c: f'{c.string},{c.header},{c.comparator}')

    @classmethod
    def fromConditionStr(cls, conditionStr: str):
        condition = cls()

        tokens = re.sub(r'((^(OR|AND) \(|\)$)| (OR|AND) )',
                        '', conditionStr).split(')(')

        condition.comparisons = {
            Comparison(*token.strip().split(','))
            for token in tokens}

        return condition


class Action:
    def __init__(self, key: str, value: str = None):
        self.key = key
        self.value = value

    def __str__(self):
        theStr = f'action="{self.key}"'

        if self.value:
            theStr += f'\nactionValue="{self.value}"'

        return theStr


class Filter:
    def __init__(self, name: str):
        self.name = name
        self.enabled = False
        self.type = "17"
        self.actions: list[Action] = list()
        self.condition = Condition()

    def __str__(self):
        tmpl = '{}="{}"'
        return '\n'.join([
            tmpl.format('name', self.name),
            tmpl.format('enabled', "yes" if self.enabled else "no"),
            tmpl.format('type', self.type),
            *[action.__str__() for action in self.actions],
            tmpl.format('condition', self.condition)
        ])
