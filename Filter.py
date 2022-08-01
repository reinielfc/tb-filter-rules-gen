from dataclasses import replace
from os import stat
import re
from typing import OrderedDict


class Comparison:
    def __init__(self, header: str, operator: str, string: str):
        self.header = header
        self.operator = operator
        self.string = string

    def __hash__(self) -> int:
        return hash(self.header) ^ hash(self.operator) ^ hash(self.string)

    def __eq__(self, other) -> bool:
        return self.string == other.string \
            and self.header == other.header \
            and self.operator == other.operator

    def __str__(self) -> str:
        return f'({self.header},{self.operator},{self.string})'


class Condition:
    def __init__(self, conditionStr: str = None, mode: str = 'OR'):
        self.mode = mode
        self.comparisons: set[Comparison] = \
            Condition.parseConditionStr(
                conditionStr) if conditionStr else set()

    def __str__(self) -> str:
        return ' '.join([f'{self.mode} {comp}' for comp in self.comparisons])

    def addComparison(self, comparison: Comparison):
        self.comparisons.add(comparison)

    @staticmethod
    def parseConditionStr(conditionStr: str) -> set[Comparison]:
        tokens = re.sub(r'(OR|AND) ', '', conditionStr).split(' ')
        return {
            Comparison(
                *re.sub(r'[()]', '', token).strip().split(',')
            ) for token in tokens
        }


class Filter:
    def __init__(self, name: str):
        self.name = name

        props = OrderedDict()
        props['name'] = name
        self.__props = props

    def __str__(self) -> str:
        template = '{}="{}"'
        return '\n'.join([
            template.format(key, prop)
            if not isinstance(prop, set)
            else '\n'.join([
                template.format(key, propItem)
                for propItem in prop])
            for (key, prop) in self.__props.items()
        ])

    def setProp(self, key: str, value: str):
        props = self.__props

        if key == 'condition':
            props[key] = Condition(value)
        elif key == 'action':
            actions = props[key] if key in props else set()
            actions.add(value)
            props[key] = actions
        else:
            props[key] = value

    def setAction(self, *values: str):
        props = self.__props
        key = 'action'

        actions = props[key] if key in props else set()
        [actions.add(action) for action in actions]

        props[key] = actions

    def replaceActions(self, *values: str):
        self.__props['action'].clear()
        self.setAction(values)

    def setConditionMode(self, mode: str):
        condition: Condition = self.__props['condition']
        condition.mode = mode

