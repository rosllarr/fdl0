import argparse
import yaml
from fedoraland.config import Config
from fedoraland.software import Software


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    subparser_install = subparsers.add_parser('install')
    subparser_install.add_argument('file', type=argparse.FileType('r'))

    subparser_init = subparsers.add_parser('init')
    subparser_init.add_argument('file', type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.subcommand == 'install':
        import fedoraland.prelude

        with open(args.file.name, 'r') as file:
            content = yaml.safe_load(file)

        for software in content:
            software = Software(**software)
            software.install()

    if args.subcommand == 'init':
        with open(args.file.name, 'r') as file:
            content = yaml.safe_load(file)

        for config in content:
            config = Config(**config)
            config.overwrite_or_create()


if __name__ == '__main__':
    main()
