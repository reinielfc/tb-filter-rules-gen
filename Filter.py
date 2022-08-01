
class ConditionItem:
    def __init__(self, header, operator, string):
        self.header = header
        self.operator = operator
        self.string = string

    def __str__(self) -> str:
        return f'({self.header},{self.operator},{self.string})'

    def __key(self):
        return (self.header, self.operator, self.string)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ConditionItem):
            return self.string == other.string \
                and self.operator == other.operator \
                and self.header == other.header

        return False
    
    def __hash__(self) -> int:
        print("__hash__: ", hash(self.__key))
        return hash(self.__key)


class Filter:
    def __init__(
        self,
        name: str,
        actions: list[str] = None,
        actionValue: str = None,
        condition: set[ConditionItem] = None,
        enabled: bool = False,
        type: int = 17,
        operator: str = "OR"
    ):
        self.name = name
        self.actionValue = actionValue

        self.enabled = enabled
        self.type = type
        self.operator = operator

        self.actions = actions if actions != None else []
        self.condition = condition if condition != None else ()

    def __str__(self) -> str:
        condition = ' '.join(
            [f'{self.operator} {conditionItem}' for conditionItem in self.condition])

        return '\n'.join([
            f'name="{self.name}"',
            f'enabled="{"yes" if self.enabled else "no"}"',
            f'type="{self.type}"',
            *[f'action="{action}"' for action in self.actions],
            f'actionValue="{self.actionValue}"',
            f'condition="{condition}"'
        ])
