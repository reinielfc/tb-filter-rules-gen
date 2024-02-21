from enum import Enum

class ActionType(Enum):
	MOVE_TO_FOLDER = ("Move to folder", True)  # Move Message to
	COPY_TO_FOLDER = ("Copy to folder", True)  # Copy Message to

	FORWARD = ("Forward", True)  # Forward Message to

	MARK_READ = "Mark read"  # Mark As Read
	MARK_UNREAD = "Mark unread"  # Mark As Unread
	MARK_FLAGGED = "Mark flagged"  # Add Star
	CHANGE_PRIORITY = ("Change priority", True)  # Set Priority to (options: Highest, High, Normal, Low, Lowest)
	ADD_TAG = ("AddTag", True)  # Tag Message
	JUNK_SCORE = ("JunkScore", True)  # Set Junk Status to (options: 0 (Not Junk), 1 (Junk))

	IGNORE_THREAD = "Ignore thread"  # Ignore Thread
	IGNORE_SUBTHREAD = "Ignore subthread"  # Ignore Subthread
	WATCH_THREAD = "Watch thread"  # Watch Thread

	STOP_EXECUTION = "Stop execution"  # Stop Filter Execution

	def __new__(cls, value: str, requires_value: bool = False):
		action_type = object.__new__(cls)
		action_type._value_ = value
		action_type.requiresValue = requires_value
		return action_type

class Priority(Enum):
	HIGHEST = "Highest"
	HIGH = "High"
	NORMAL = "Normal"
	LOW = "Low"
	LOWEST = "Lowest"


class JunkScore(Enum):
	JUNK = 1
	NOT_JUNK = 0

class ActionValueMissingException(BaseException): "Action is missing value."

class Action:
	def __init__(self, action: ActionType, value: str = None):
		self.action: ActionType = action
		
		if action.requires_value and value == None:
			raise ActionValueMissingException(f"Action '{action.value}' is missing value.")

		self.value = value