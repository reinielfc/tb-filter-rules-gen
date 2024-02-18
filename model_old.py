import itertools
import textwrap
from pathlib import Path

import yaml
from jinja2 import Template
from pydantic import BaseModel, Field


class MsgFilterRulesModel(BaseModel):
    @staticmethod
    def rule_str(key, value) -> str:
        return f'{key}="{value}"'

    def rules(self) -> list[str]:
        return [Header.rule_str(key, value) for key, value in self.dict().items()]


class Header(MsgFilterRulesModel):
    version: str = '9'
    logging: str = 'no'


class Action(MsgFilterRulesModel):
    action: str
    action_value: str = Field(None, alias='value')

    def rules(self):
        rules = [Action.rule_str('action', self.action)]

        if self.action_value:
            rules.append(Action.rule_str('actionValue', self.action_value))

        return rules


class Condition(MsgFilterRulesModel):
    operator: str = 'OR'
    criteria: list[str]

    def condition_str(self):
        op = self.operator
        sorted_criteria = sorted(self.criteria, key=lambda x: x.split(',')[2])
        return f'{op} (' + f') {op} ('.join(sorted_criteria) + ')'

    def rules(self):
        return [Condition.rule_str('condition', self.condition_str())]


class Filter(MsgFilterRulesModel):
    name: str
    enabled: str = 'yes'
    filter_type: int = Field(17, alias='type')
    actions: list[Action]
    condition: Condition

    def rules(self):
        rules = [
            Filter.rule_str('name', self.name),
            Filter.rule_str('enabled', self.enabled),
            Filter.rule_str('type', self.filter_type)
        ]

        for action in self.actions:
            rules += action.rules()

        return rules + self.condition.rules()


class MsgFilterRules(MsgFilterRulesModel):
    header: Header = Header()
    filters: list[Filter]

    @staticmethod
    def load_yaml_str(file_path):
        with open(file_path, 'r') as f:
            return f.read()

    @staticmethod
    def render_yaml_template(tmpl_str: str, context=dict()):
        tmpl_render = Template(tmpl_str).render(context)
        return yaml.safe_load(tmpl_render)

    @staticmethod
    def from_file(file_path: Path) -> 'MsgFilterRules':
        yaml_string = MsgFilterRules.load_yaml_str(file_path)
        yaml_render = MsgFilterRules.render_yaml_template(
            yaml_string, context=yaml.safe_load(yaml_string))
        return MsgFilterRules(**yaml_render)

    @staticmethod
    def dat(file_path: Path):
        return MsgFilterRules.from_file(file_path).dat_str()

    def dat_str(self):
        return '\n'.join(self.rules())

    def rules(self):
        return self.header.rules() + \
            [rule for filter in self.filters for rule in filter.rules()]
