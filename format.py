from argparse import ArgumentParser
from datetime import datetime
from subprocess import run
from sys import stdin, stdout

from jsonlines import Reader, Writer
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser(
        prog='format',
        description='Format Verilog code',
        epilog=f'Copyright (c) {datetime.now().year} - HDLOJ',
    )

    return parser.parse_args()


def main():
    parse_args()

    with Reader(stdin) as reader:
        sources = tuple(reader)

    formatted_sources = []

    for source in tqdm(sources):
        try:
            process = run(
                'verible-verilog-format -',
                input=source,
                text=True,
                capture_output=True,
                shell=True,
            )
        except UnicodeDecodeError:
            pass
        else:
            formatted_source = process.stdout

            formatted_sources.append(formatted_source)

    with Writer(stdout) as writer:
        writer.write_all(formatted_sources)


if __name__ == '__main__':
    main()
