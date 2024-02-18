from pydantic import BaseModel


class MsgFilterRulesBaseModel(BaseModel):

    @staticmethod
    def _as_rule_str(key, value) -> str:
        return f'{key}="{value}"'

    def rules(self) -> list[str]:
        return list()
