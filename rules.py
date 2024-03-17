class Rules:
    def rules(self) -> list[str]:
        pass

    @staticmethod
    def rulestr(**kwargs) -> str:
        key, value = list(kwargs.items())[0]

        return f'{key}="{value}"'

    def __str__(self):
        return "\n".join(self.rules())
