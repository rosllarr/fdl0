import argparse
import yaml
from fedoraland.usecase.binary_download import BinaryDownload
from fedoraland.usecase.package_manager import PackageManager
# from fedoraland.config import Config
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

    call_stack = list()

    if args.subcommand == 'install':
        # import fedoraland.prelude

        with open(args.file.name, 'r') as file:
            contents = yaml.safe_load(file)

        for content in contents:
            attr = Parser(**content)
            kind = attr.get("kind")

            if kind == "packageManager":
                app = PackageManager(**attr, call_stack=call_stack)
                app.install()

            if kind == "binaryDownload":
                app = BinaryDownload(**attr, call_stack=call_stack)
                app.install()

            if kind == "gitClone":
                app = BinaryDownload(**attr, call_stack=call_stack)
                app.install()

        # parser = Parser(content)
        # for app in parser.apps:
        #     app.install(call_stack)

    # if args.subcommand == 'init':
    #     with open(args.file.name, 'r') as file:
    #         content = yaml.safe_load(file)

    #     for config in content:
    #         config = Config(**config)
    #         config.overwrite_or_create()

    # if args.subcommand == 'sync':
    #     with open(args.file.name, 'r') as file:
    #         content = yaml.safe_load(file)

    #     for config in content:
    #         config = Config(**config)
    #         config.sync()

    # Display results
    for stack in call_stack:
        print(stack)


if __name__ == '__main__':
    main()
