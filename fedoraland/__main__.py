import argparse
import yaml
from fedoraland.config import Config
from fedoraland.usecase.parser import Parser
# from fedoraland.software import Software


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    subparser_install = subparsers.add_parser('install')
    subparser_install.add_argument('file', type=argparse.FileType('r'))

    subparser_init = subparsers.add_parser('init')
    subparser_init.add_argument('file', type=argparse.FileType('r'))

    subparser_init = subparsers.add_parser('sync')
    subparser_init.add_argument('file', type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.subcommand == 'install':
        # import fedoraland.prelude

        with open(args.file.name, 'r') as file:
            content = yaml.safe_load(file)

        parser = Parser(content)
        for app in parser.apps:
            app.install()

    if args.subcommand == 'init':
        with open(args.file.name, 'r') as file:
            content = yaml.safe_load(file)

        for config in content:
            config = Config(**config)
            config.overwrite_or_create()

    if args.subcommand == 'sync':
        with open(args.file.name, 'r') as file:
            content = yaml.safe_load(file)

        for config in content:
            config = Config(**config)
            config.sync()


if __name__ == '__main__':
    main()
