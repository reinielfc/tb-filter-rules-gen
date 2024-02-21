from aenum import Enum


class Enabled(Enum):
	YES = "yes"
	NO = "no"


class FilterType(Enum):
	MANUALLY_RUN = 16
	GETTING_NEW_MAIL_FILTER_BEFORE_JUNK_CLASSIFICATION = 1
	GETTING_NEW_MAIL_FILTER_AFTER_JUNK_CLASSIFICATION = 32
	ARCHVIVING = 128
	AFTER_SAVING = 64
	PERIODICALLY_EVERY_10_MINUTES = 256
	DEFAULT = MANUALLY_RUN + GETTING_NEW_MAIL_FILTER_AFTER_JUNK_CLASSIFICATION




class Filter:
	name: str
	enabled: str = Enabled.YES
	filter_type: int = FilterType.DEFAULT
	actions: list[Action]
