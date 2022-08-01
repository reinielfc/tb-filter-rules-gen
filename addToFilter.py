from cmath import log
from getopt import getopt
import sys
from Filter import ConditionItem, Filter

from parseFilterList import parseFiltersFile

argv = sys.argv[2:]

# try:
#     opts, args = getopt(argv, "gf")
# except:
#     print("error")

with open(sys.argv[1]) as file:
    version, logging, filters = parseFiltersFile(file)
    print(f'version="{version}"')
    print(f'logging="{logging}"')

    myFilter: Filter = filters['com.live.reyfdz96 » finances']

    myFilter.condition.add(
        ConditionItem("from", "contains", "alertnotifications@message.truist.com")
    )

    print(">>> hash(): ", 
    )

    [print(filter) for (name, filter) in filters.items()]