import yaml

from msg_filter_rules.base_model import MsgFilterRulesBaseModel
from msg_filter_rules.filter import ConditionList


class Filter(MsgFilterRulesBaseModel):
    name: str
    enabled: bool
    type: int
    actions: list[str | dict]
    conditions: list[ConditionList]

    def actions_rules(self):
        def action_as_rules(action):
            if isinstance(action, dict):
                action = next(iter(action.items()))
                return Filter._as_rule_str('action', action[0]), Filter._as_rule_str('actionValue', action[1])
            else:
                return (Filter._as_rule_str('action', action),)

        return (action_rule
                for action in self.actions
                for action_rule in action_as_rules(action))

    def rules(self):
        return (
            MsgFilterRulesBaseModel._as_rule_str('name', self.name),
            MsgFilterRulesBaseModel._as_rule_str('enabled', {True: 'yes', False: 'no'}[self.enabled]),
            MsgFilterRulesBaseModel._as_rule_str('type', str(self.type)),
            *self.actions_rules(),
            # Filter._as_rule_str('condition', )
        )


if __name__ == '__main__':
    data = """
    name: test
    enabled: yes
    type: 17
    actions:
        - test 1
        - test: 2
    conditions:
        - or: 
            - from,ends with,technewsletter.com
            - from,ends with,industryupdate.com
            - from,ends with,exampleinsights.com
            - and: ["from,ends with,test.com", "subject,is,This is a test"]
    """

    parsed_data = yaml.safe_load(data)
    model = Filter(**parsed_data)

    print(model)
    for c in model.conditions:
        print(c.criteria_list)

    for rule in model.rules():
        print(rule)
