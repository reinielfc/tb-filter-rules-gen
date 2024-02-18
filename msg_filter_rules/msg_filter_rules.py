from msg_filter_rules.base_model import MsgFilterRulesBaseModel
from msg_filter_rules.filter import Filter


class MsgFilterRules(MsgFilterRulesBaseModel):
    header: dict
    filters: list[Filter]
