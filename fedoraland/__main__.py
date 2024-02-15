import argparse


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")

    subparser_install = subparsers.add_parser('install')
    subparser_install.add_argument('file', type=argparse.FileType('r'))

    args = parser.parse_args()

    if args.subcommand == 'install':
        with open(args.file.name, 'r') as f:
            for line in f:
                print(line)


if __name__ == '__main__':
    main()
