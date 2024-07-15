from argparse import ArgumentParser
from datetime import datetime
from sys import stdin, stdout

from jsonlines import Reader, Writer


def parse_args():
    parser = ArgumentParser(
        prog='stats',
        description='Get statistics on local code data.',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    parser.add_argument(
        'line_limit',
        type=int,
        help='limit on a module\'s number of lines',
    )

    return parser.parse_args()


def main():
    args = parse_args()

    with Reader(stdin) as reader:
        modules = tuple(reader)

    with Writer(stdout) as writer:
        for module in modules:
            line_count = len(module.split('\n'))

            if line_count <= args.line_limit:
                writer.write(module)


if __name__ == '__main__':
    main()
