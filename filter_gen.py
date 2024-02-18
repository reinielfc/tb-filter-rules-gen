import argparse

from pathlib import Path


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='tb_filter_rules_gen',
        description='Generate filter rules for Thunderbird')

    parser.add_argument(
        dest='file', metavar='FILE', type=Path,
        help='config file')

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    yaml_file: Path = args.file
