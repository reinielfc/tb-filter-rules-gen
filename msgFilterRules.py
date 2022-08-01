import argparse
from curses import meta
from typing import OrderedDict

from Filter import Filter


class ParseProps(argparse.Action):
    def __call__(
            self, parser, namespace,
            values, option_string=None):
        setattr(namespace, self.dest, OrderedDict())

        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value


def getArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Generate filter rules for Thunderbird')

    parser.add_argument(
        '-n', metavar='<name>', dest='name', type=str, required=True,
        help='name of rule to add or modify')

    parser.add_argument(
        '-r', '--replace', dest="do_replace_action", action='store_true',
        help='replace pre-existing actions')

    parser.add_argument(
        '-v', metavar='<action-value>', dest='action_value', type=str,
        help='path to destination of filtered items')

    parser.add_argument(
        '-m', metavar='<mode>', dest="mode", type=str, choices=['OR', 'AND'], default='OR',
        help='mode of operation, on condition (OR by default)')

    parser.add_argument(
        '-c', dest='condition_file', type=str,
        help='condition CSV file to parse, has 3 columns: EmailHeader,Operator,String')

    parser.add_argument(
        '-p', metavar='<key=value>', dest='props', nargs='*', action=ParseProps,
        default=OrderedDict([('enabled', 'yes'), ('type', '17')]),
        help='additional properties, by default: enabled=yes, type=17')

    parser.add_argument(
        '-f', metavar='<rules-file>', dest='rules_file', type=str,
        help='path to pre-existing msgFilterRules.dat file')

    return parser.parse_args()


def getFilterFromFile(filePath: str, filterName: str) -> tuple[Filter, str]:
    filterRulesFile = open(filePath, 'r')

    theFilter = None
    template = []

    curFilter = None
    for line in filterRulesFile:
        key, value = line.partition("=")[::2]
        value = value[1:-2]  # remove quotes from value

        # print(f'{key}={value}')

        if key == 'name':
            if value == filterName:
                template.append('{}\n')
                curFilter = Filter(value)
            else:
                template.append(line)
                theFilter = curFilter
                curFilter = None           
        elif curFilter:
            curFilter.setProp(key, value)
        else:
            template.append(line)

    filterRulesFile.close()
    return theFilter or curFilter, ''.join(template)


def processArgs(args: argparse.Namespace):
    rulesFile = args.rules_file
    name = args.name

    theFilter, template = getFilterFromFile(rulesFile, name) if rulesFile \
        else (Filter(name), 'version="9"\nlogging="no"\n{}\n')

    props: OrderedDict = args.props
    for (key, value) in props.items():
        theFilter.setProp(key, value)

    actions = args.action
    actions and theFilter.replaceActions(actions) \
        if args.do_replace_action \
        else theFilter.setAction(actions)

    actionValue = args.action_value
    actionValue and theFilter.setProp('actionValue', actionValue)

    mode = args.mode
    mode and theFilter.setConditionMode(mode)

    print(template.format(theFilter or ''), end='')


args = getArgs()
processArgs(args)
