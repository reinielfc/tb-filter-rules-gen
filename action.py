from .rules import Rules
from enum import Enum


class Action(Rules):
    def __init__(self, action: str, value: str = None) -> None:
        self._action = action
        self._value = value

    def rules(self) -> list[str]:
        rules = [self.rulestr(action=self._action)]

        if self._value != None:
            rules.append(self.rulestr(actionValue=self._value))

        return rules


class Priority(Enum):
    HIGHEST = "Highest"
    HIGH = "High"
    NORMAL = "Normal"
    LOW = "Low"
    LOWEST = "Lowest"

class Tag(Enum):
    REVIEW = "🔍 Review"
    UPDATE = "⬆️ Update"
    IMPORTANT = "❗IMPORTANT"

class JunkScore(Enum):
    JUNK = 1
    NOT_JUNK = 0


class ActionFunction:
    @staticmethod
    def action(action: str):
        return lambda: Action(action)

    @staticmethod
    def actionwithvalue(action: str):
        return lambda v: Action(action, v)

    @staticmethod
    def actionwithpriority(action: str):
        def f(value: Priority):
            return Action(action, value)

        return f

    def actionwithtag(action: str):
        def f(value: Tag | str):
            return Action(action, value)

        return f

    @staticmethod
    def actionwithjunkscore(action: str):
        def f(value: JunkScore):
            return Action(action, value)

        return f



class ActionBuilder:
    movetofolder = ActionFunction.actionwithvalue("Move to folder")  # Move Message To
    copytofolder = ActionFunction.actionwithvalue("Copy to folder")  # Copy Message to

    forward = ActionFunction.actionwithvalue("Forward")  # Forward Message to

    markread = ActionFunction.action("Mark read")  # Mark As Read
    markunread = ActionFunction.action("Mark unread")  # Mark As Unread
    markflagged = ActionFunction.action("Mark flagged")  # Add Star
    changepriority = ActionFunction.actionwithpriority("Change priority")  # Set Priority to (options: Highest, High, Normal, Low, Lowest)
    addtag = ActionFunction.actionwithtag("AddTag")  # Tag Message
    junkscore = ActionFunction.actionwithjunkscore("JunkScore")  # Set Junk Status to (options: 0 (Not Junk), 1 (Junk))

    ignorethread = ActionFunction.action("Ignore thread")  # Ignore Thread
    ignoresubthread = ActionFunction.action("Ignore subthread")  # Ignore Subthread
    watchthread = ActionFunction.action("Watch thread")  # Watch Thread

    stopexecution = ActionFunction.action("Stop execution")  # Stop Filter Execution
