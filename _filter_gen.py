import argparse

from pathlib import Path
from model import MsgFilterRules


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
    rules_dat: str = MsgFilterRules.dat(yaml_file)

    dat_file = yaml_file.with_suffix('.dat')

    print(f"{yaml_file} -> {dat_file}")

    with open(dat_file, 'w') as f:
        f.write(rules_dat)
