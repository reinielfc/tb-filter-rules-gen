import re
from io import TextIOWrapper

from Filter import ConditionItem, Filter


def parseFiltersFile(file: TextIOWrapper) -> tuple[str, str, dict[Filter]]:
    version = "9"
    logging = "no"
    filters: dict[Filter] = {}

    currentFilter: Filter = None
    for line in file:
        name, value = line.partition("=")[::2]
        value = value[1:-2]

        if name == 'version':
            version = value
        elif name == 'logging':
            logging = value
        elif name == 'name':
            currentFilter = Filter(value)
            filters[value] = currentFilter
        elif (name == 'enabled'):
            currentFilter.enabled = (value == 'yes')
        elif (name == 'type'):
            currentFilter.type = int(value)
        elif (name == 'action'):
            currentFilter.actions.append(value)
        elif (name == 'actionValue'):
            currentFilter.actionValue = value
        elif (name == 'condition'):
            currentFilter.condition = {
                ConditionItem(*re.sub(r'[()]', '', token).strip().split(','))
                for token in value.replace('OR ', '').split(' ')
            }

    filters[currentFilter.name] = currentFilter

    return version, logging, filters
