from msg_filter_rules.base_model import MsgFilterRulesBaseModel


class Condition(MsgFilterRulesBaseModel):
    op: 

class ConditionList(MsgFilterRulesBaseModel):
    criteria: list[str | Condition]

