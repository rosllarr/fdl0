import argparse
import yaml

from fedoraland.software import Software

import fedoraland.prelude


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    subparser_install = subparsers.add_parser('install')
    subparser_install.add_argument('file', type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.subcommand == 'install':
        with open(args.file.name, 'r') as file:
            content = yaml.safe_load(file)

        for software in content:
            software = Software(**software)
            software.install()


if __name__ == '__main__':
    main()
