#!/usr/bin/env python

import argparse
from collections import OrderedDict
from curses import meta
import pathlib

from Filter import Action, Comparison, Condition, Filter


class KeyValueArg(argparse.Action):
    def __call__(
            self, parser, namespace,
            values, option_string=None):
        setattr(namespace, self.dest, OrderedDict())

        for value in values:
            key, value = "=" in value \
                and value.split('=') \
                or (value, None)

            getattr(namespace, self.dest)[key] = value


def getArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='msgFilterRules.py',
        description='Generate filter rules for Thunderbird')

    parser.add_argument(
        '-name', metavar='<name>', required=True, type=str,
        help='name of rule to add or modify')

    parser.add_argument(
        '-type', metavar='<type>', type=str, default='17',
        help='set rule type')

    parser.add_argument(
        '-disabled', action='store_true',
        help='set filter as disabled')

    parser.add_argument(
        '-actions', metavar='<action>', nargs='*', action=KeyValueArg,
        help='actions to perform (in order), key=value if action has value')

    parser.add_argument(
        '-condition-file', metavar='<file>', type=str,
        help='CSV file with comparisons to add, columns: <email header>,<comparison>,<string>')

    parser.add_argument(
        '-mode', metavar='<mode>', choices=['OR', 'AND'], type=str, default='OR',
        help='mode of operation in condition, default: OR')

    parser.add_argument(
        '-rules-file', metavar='<file>', type=str,
        help='path to pre-existing msgFilterRules.dat file')

    return parser.parse_args()


def getFilterFromFile(filePath: str, filterName: str) -> tuple[Filter, str]:
    rulesFile = open(filePath, 'r')
    line = rulesFile.readline()

    theFilter: Filter = None
    template = []

    lastAction = None
    while line:
        key, value = line.partition('=')[::2]

        if key == 'name':
            value = value[1:-2]
            if value == filterName:
                template.append('{}\n')
                theFilter = Filter(value)
            else:
                template.append(line)
                if theFilter:
                    break
        elif theFilter:
            value = value[1:-2]

            if key == 'action':
                lastAction = Action(value)
                theFilter.actions.append(lastAction)
            elif key == 'actionValue':
                lastAction.value = value
            elif key == 'condition':
                theFilter = Condition.fromConditionStr(value)
            else:
                theFilter.props[key] = value
        else:
            template.append(line)

        line = rulesFile.readline()

    template.extend(rulesFile.readlines())

    rulesFile.close()
    return theFilter, ''.join(template)


def addCondtionFileToFilter(filePath: str, theFilter: Filter):
    comparisons = theFilter.condition.comparisons
    with open(filePath, 'r') as conditionFile:
        [comparisons.add(Comparison(*line.strip().split(',')))
         for line in conditionFile]


def processArgs(args: argparse.Namespace):
    name = args.name
    rulesFile = args.rules_file

    if rulesFile:
        theFilter, theTemplate = getFilterFromFile(rulesFile, name)

        if theFilter is None:
            theFilter = Filter(name)
            theTemplate += '{}\n'
    else:
        theFilter = Filter(name)
        theTemplate = 'version="9"\nlogging="no"\n{}\n'

    theFilter.type = args.type
    theFilter.enabled = not args.disabled

    if actions := args.actions:
        theFilter.actions = [Action(*item) for item in actions.items()]

    if conditionFile := args.condition_file:
        with open(conditionFile) as conditionFile:
            theFilter.condition.comparisons = \
                {Comparison(*line.strip().split(',')) for line in conditionFile}

    theFilter.condition.mode = args.mode

    print(theTemplate.format(theFilter or ''), end='')


args = getArgs()
processArgs(args)
