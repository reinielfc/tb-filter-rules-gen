from .action import ActionBuilder as ACT, JunkScore, Priority
from .filter import Filter, FilterType, FilterList
from .comparison import ComparisonListBuilder as PROP

SENDER = PROP.sender
SUBJECT = PROP.subject
PROPX = PROP.expressionsearch